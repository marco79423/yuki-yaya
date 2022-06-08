# Yuki-YaYa

簡易壓圖小工具

## 功能

* 自動將照片轉檔為 JPG，並且統一副檔名為 `.jpg` (也可以轉為 Webp)
* 調整照片尺寸改為長寬最大邊為 1440px (預設，可修改)
* 壓縮照片大小直至 300 KB 以下 (預設，可修改)
* 自動加浮水印

(不要問我規則為啥是這樣，女友領導要求的)

## 操作說明

將 Yuki-YaYa 執行檔放在預處理照片的資料夾，接著點兩下即可。

Yuki-YaYa 會自動處理當前資料夾的照片，並輸出到「輸出」資料夾裡。

## 設定檔

```yaml
logo:
  enabled: true
  filepath: logo.png
output:
  max_size: 300  # 單位是 KB

  max_width: 1440
  max_height: 1440

  to_jpg: true
  to_webp: true
```

## 加浮水印

在同一資料夾中，放上指定路徑的圖片就可以加上浮水印，也可以透過修改設定檔決定不同的路徑。

    目標資料夾/
        圖片1.jpg
        圖片2.png
        ...

        .yuki-yaya/
            logo.png  # 就會在右下角加上 logo.png 的浮水印
