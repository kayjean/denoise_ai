denoise分成數學方式和AI方式

數學方式很單純，除了medianfilter外，就是加入簡單的cali.png校正，程式參考MedianFilter.py

AI方式是從github tensorflow dncnn直接下載範例使用 區分為三大類
1. color image with gauss smear 原本範例程式，當成學習基礎，範例結果看起來還不錯
2. convert colorful chart image to greyscale with gauss smear
	結果分析 original 1550 images : 改善效果很少
	結果分析 處理過的 1550 images : 效果很平滑很好
3. convert colorful chart image to greyscale with calibration smear image
	結果分析 original 1550 images : 直接穿透的那張效果很平滑很好，反射影像很糟糕應該是沒有訓練過
	結果分析 處理過的 1550 images : 效果很平滑很好

執行上，以最後一類為例子
source activate tensorflow
cd directory
python addnoise_mono_calibration.py (共有三種不同的addnoise  calibration的觀念很簡單，就是把亮點直接拷貝到位置上)
python main.py --batch_size 64 (為了避免當機 嘗試改成48比較不會當)
python main.py --phase test