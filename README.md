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
%%{init: {"flowchart": {"curve": "linear"}} }%%
flowchart TB

%% ================ Core config ================
cfg[uv/UV_config.py]

%% ==================== Data ====================
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

%% ================== Training ==================
subgraph Training
  dd[uv/UV_driving_data.py]
  model[uv/UV_model.py]
  train[uv/UV_train.py]
  ckpt[(save/model.ckpt)]
end

%% ========= Evaluation / Visualization =========
subgraph Evaluation
  sim[uv/UV_simulate.py]
  t_an[uv/UV_train_analysis.py]
  feat[uv/UV_feature_view.py]
end

%% ================== Runtime ===================
subgraph Runtime
  airun[uv/UV_airun.py]
  camera[(CSI/USB Camera 320x240)]
  robot[(JetBot Robot)]
end

%% ============== Optional Hardware =============
subgraph Hardware
  xhat[uv/UV_xhat.py]
  opi[uv/UV_opidistance3.py]
end


%% -------- Data collection / prep --------
cfg -->|read outputDir, currentDir| kb
kb -->|append rows: filename, wheel 0..4| data_csv
kb -->|save BGR image to jpg| data_imgs
kb -->|write wheel, recording, cnt| cfg

d_an -->|read csv, count classes| data_csv
cfg -->|read currentDir, modelheight| d_an

d_up -->|read csv, upsample 1..4, append| data_csv
cfg -->|read currentDir| d_up

d_dc -->|flip images, write dc_*.jpg| data_imgs
d_dc -->|rewrite csv: remove dc_*, append mapped labels| data_csv
cfg -->|read currentDir, use writer| d_dc

d_del -->|recreate data dirs, empty csv| data_csv
d_del -->|recreate logs| logs


%% ------------- Training pipeline -------------
data_csv -->|xs filenames, ys labels| dd
data_imgs -->|images by xs| dd
cfg -->|read currentDir, modelheight| dd
dd -->|batch: x 66x200x3 div255, y int| train

train -->|feed x, y, keep_prob| model
model -->|logits N by 5| train
train -->|save checkpoint| ckpt
train -->|write summaries loss| logs


%% -------- Evaluation / Visualization --------
ckpt -->|restore| sim
ckpt -->|restore| t_an
ckpt -->|restore| feat

data_csv -->|filenames, labels| sim
data_imgs -->|rgb to 66x200, div255| sim
cfg -->|read outputDir, currentDir, modelheight| sim
sim -->|feed image| model
model -->|argmax to class| sim

data_csv -->|filenames, labels| t_an
data_imgs -->|rgb to 66x200, div255| t_an
cfg -->|read outputDir, currentDir, modelheight| t_an
t_an -->|feed image| model
model -->|per class accuracy| t_an

data_csv -->|filenames only| feat
data_imgs -->|rgb to 66x200, div255| feat
cfg -->|read outputDir, currentDir, modelheight| feat
feat -->|feed image| model
model -->|feature maps and logits| feat


%% ----------------- Runtime -------------------
camera -->|frames BGR 320x240| airun
airun -->|crop by modelheight, resize 66x200, div255| model
model -->|softmax argmax to wheel| airun
airun -->|robot cmd fwd left right stop| robot
cfg -->|read ai_speed, write wheel| airun

%% ------------- Optional hardware -------------
opi -.->|get distance cm| airun
xhat -.->|motor_one_speed 0..100| kb
xhat -.->|motor_one_speed 0..100| airun

```
