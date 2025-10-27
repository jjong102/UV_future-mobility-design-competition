# UV_future-mobility-design-competition
UV 팀 미래 모빌리티 경진 대회 (인천대학교 공학교육혁신 센터)

## 딥 러닝을 활용한 운전자의 주행 학습

### Manual
0. uv 폴더를 다운받은 뒤 터미널 실행 후 작업공간으로 이동한다.
```
cd uv
```
1. keyboard.py를 실행 시켜 주행 데이터를 수집한다.( sudo password : jetbot )
```
sudo python3 keyboard.py
```
1.1 's'버튼 키보드 조작, 'r' 데이터 기록 버튼,

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'&#8592;': 좌회전, '&#8593;': 전진, '&#8594;': 우회전, '&#8595;': 3초 정지 후 출발 



2. 수집된 데이터의 비율를 조정하기 위해 decalcom.py, data_upsampling.py를 실행 한다. 이때 data_analysis.py를 사용하여 각 방향에 대한 비율을 적절히 조정한다.

```
sudo python3 decalcom
sudo python3 data_analysis
sudo python3 data_upsampling
```

3. train.py를 실행하여 현재 샘플링한 데이터를 기반으로 model을 학습시킨다.
```
sudo python3 train.py
```

4. airun.py를 통해 저장된 model을 실행 시킬수 있다. ( 카메라 화면 켜진 후 a 버튼으로 자율주행 시작 )
```
sudo python3 airun.py
```


*** 이미 학습된 모델이 있으므로 4단계를 실행 하시면 됩니다.

## 코드 구조
```mermaid
%%{init: {'flowchart': {'curve': 'step'}} }%%
flowchart TB

%% Core config (shared state/params)
cfg[uv/UV_config.py]

%% Data collection / prep
subgraph Data
  kb[uv/UV_keyboard.py]
  d_an[uv/UV_data_analysis.py]
  d_up[uv/UV_data_upsampling.py]
  d_dc[uv/UV_decalcom.py]
  d_del[uv/UV_data_delete.py]
  data_csv[(data/<currentDir>/data.csv)]
  data_imgs[(data/<currentDir>/*.jpg)]
  logs[(./logs)]
end

%% Training
subgraph Training
  dd[uv/UV_driving_data.py]
  model[uv/UV_model.py]
  train[uv/UV_train.py]
  ckpt[(save/model.ckpt)]
end

%% Evaluation / Visualization
subgraph Evaluation
  sim[uv/UV_simulate.py]
  t_an[uv/UV_train_analysis.py]
  feat[uv/UV_feature_view.py]
end

%% Runtime (Autonomous driving)
subgraph Runtime
  airun[uv/UV_airun.py]
  camera[(CSI/USB Camera 320x240)]
  robot[(JetBot Robot)]
end

%% Optional hardware (commented integrations)
subgraph Hardware
  xhat[uv/UV_xhat.py]
  opi[uv/UV_opidistance3.py]
end

%% ---------- Data I/O with values on edges ----------

%% Keyboard data collection
kb -->|append rows: (filename, cfg.wheel ∈ {0,1,2,3,4})| data_csv
kb -->|save BGR image: full_image→.jpg| data_imgs

%% Config usage by keyboard
cfg -->|read: outputDir, currentDir| kb
kb -->|write: wheel, recording, cnt; open: f/fwriter| cfg

%% Data analysis / upsampling / decalcom
d_an -->|read CSV: filenames, labels; print class counts| data_csv
cfg -->|read: currentDir, modelheight| d_an

d_up -->|read CSV; upsample classes 1..4; append rows| data_csv
cfg -->|read: currentDir| d_up

d_dc -->|flip images→write dc_*.jpg| data_imgs
d_dc -->|rewrite CSV (remove dc_*) + append (dc_name, mapped label 1↔3, 2→2)| data_csv
cfg -->|read: currentDir; use fwriter| d_dc

d_del -->|delete+recreate training dir + empty CSV| data_csv
d_del -->|delete+recreate logs dir| logs

%% Driving data loader
data_csv -->|paths xs[], labels ys[]| dd
data_imgs -->|image files at xs[]| dd
cfg -->|read: currentDir, modelheight| dd
dd -->|batch: x float32[N,66,200,3]/255, y int[N,1]| train
%%{init: {'flowchart': {'curve': 'step'}} }%%
flowchart TB

%% Core config
cfg[uv/UV_config.py]

%% Data collection / prep
subgraph Data
  kb[uv/UV_keyboard.py]
  d_an[uv/UV_data_analysis.py]
  d_up[uv/UV_data_upsampling.py]
  d_dc[uv/UV_decalcom.py]
  d_del[uv/UV_data_delete.py]
  data_csv[(data/currentDir/data.csv)]
  data_imgs[(data/currentDir/*.jpg)]
  logs[(./logs)]
end

kb -->|append rows filename and wheel 0..4| data_csv
kb -->|save image jpg from full_image| data_imgs

cfg -->|read outputDir currentDir| kb
kb -->|write wheel recording cnt open f and fwriter| cfg

d_an -->|read csv and count classes| data_csv
cfg -->|read currentDir modelheight| d_an

d_up -->|read csv upsample classes 1..4 append| data_csv
cfg -->|read currentDir| d_up

d_dc -->|flip images write dc jpg| data_imgs
d_dc -->|rewrite csv remove dc then append mapped labels| data_csv
cfg -->|read currentDir use fwriter| d_dc

d_del -->|delete recreate data training and empty csv| data_csv
d_del -->|delete recreate logs| logs

%% Training
subgraph Training
  dd[uv/UV_driving_data.py]
  model[uv/UV_model.py]
  train[uv/UV_train.py]
  ckpt[(save/model.ckpt)]
end

data_csv -->|xs filenames ys labels| dd
data_imgs -->|image files by xs| dd
cfg -->|read currentDir modelheight| dd
dd -->|batch x 66x200x3 float div255 and y int| train

train -->|feed x y_ keep_prob| model
model -->|logits y n by 5| train
train -->|save checkpoint| ckpt
train -->|write tf summaries loss| logs

%% Evaluation / Visualization
subgraph Evaluation
  sim[uv/UV_simulate.py]
  t_an[uv/UV_train_analysis.py]
  feat[uv/UV_feature_view.py]
end

ckpt -->|restore variables| sim
ckpt -->|restore variables| t_an
ckpt -->|restore variables| feat

data_csv -->|filenames labels| sim
data_imgs -->|rgb image to 66x200 div255| sim
cfg -->|read outputDir currentDir modelheight| sim
sim -->|feed image| model
model -->|logits argmax predicted class| sim

data_csv -->|filenames labels| t_an
data_imgs -->|rgb image to 66x200 div255| t_an
cfg -->|read outputDir currentDir modelheight| t_an
t_an -->|feed image| model
model -->|logits for accuracy by class| t_an

data_csv -->|filenames| feat
data_imgs -->|rgb image to 66x200 div255| feat
cfg -->|read outputDir currentDir modelheight| feat
feat -->|feed image| model
model -->|h_conv feature maps and logits| feat

%% Runtime
subgraph Runtime
  airun[uv/UV_airun.py]
  camera[(CSI USB Camera 320x240)]
  robot[(JetBot Robot)]
end

camera -->|frames bgr 320x240| airun
airun -->|crop by modelheight resize 66x200 div255| model
model -->|logits softmax argmax to wheel| airun
airun -->|robot forward left right stop| robot
cfg -->|read ai speed write wheel| airun

%% Optional hardware
subgraph Hardware
  xhat[uv/UV_xhat.py]
  opi[uv/UV_opidistance3.py]
end

opi -.->|get_distance cm| airun
xhat -.->|motor_one_speed 0..100| kb
xhat -.->|motor_one_speed 0..100| airun

```
