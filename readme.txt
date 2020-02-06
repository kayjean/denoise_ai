從github tensorflow dncnn直接下載範例使用 區分為三大類

1. color image with gauss smear
2. convert colorful chart image to greyscale with gauss smear
3. convert colorful chart image to greyscale with calibration smear image

結果分析
1. color : 範例結果看起來還不錯
2. chart with gauss smear vs original 1550 images : 不太能看
3. chart with gauss smear vs 處理過的 1550 images : 效果很平滑很好
4. chart with calibration smear vs original 1550 images : 還不錯
5. chart with calibration smear vs 處理過的 1550 images : 效果很平滑很好

執行方式，分成三大類

color
monochrome + gauss

步驟
source activate tensorflow
cd directory
python addnoise.py   (共有三種不同的addnoise)
python main.py --batch_size 64 (為了避免當機 嘗試改成48 效果不確定)
python main.py --phase test