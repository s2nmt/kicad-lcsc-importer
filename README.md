# LCSC Importer for KiCad

Plugin cho KiCad 10 trên Windows. Nhập mã LCSC để xuất symbol, footprint và model 3D (nếu có) vào thư viện `maruyama`.

## Cài và sử dụng

1. Tải `lcsc-importer-pcm.zip` trong **Releases** của repo.
2. Trong KiCad Manager, mở **Plugin and Content Manager → Install from File…** và chọn ZIP. Nếu KiCad yêu cầu gỡ bản cũ trước, chọn **Uninstall**, rồi bấm **Apply Pending Changes**.
3. Trong **Preferences → Plugins**, bật **Enable KiCad API**. Giữ Python đi kèm KiCad. KiCad cài dependency vào môi trường riêng của plugin ở lần nạp đầu.
4. Mở lại PCB Editor và tìm nút mũi tên trắng nền xanh **Import LCSC** trên thanh công cụ. Nhập mã như `C116151` và bấm **Import**.
5. Đăng ký `maruyama.kicad_sym` và `maruyama.pretty` trong bảng thư viện tương ứng với nickname `maruyama`. Mặc định plugin xuất vào `Documents/KiCad/10.0/libs`. Trong **Preferences → Configure Paths…**, đặt `MARUYAMA_3D` trỏ tới thư mục `maruyama.3dshapes` bên trong thư mục xuất.

Nếu linh kiện dùng chung footprint, trình chuyển đổi có thể dừng khi gặp file trùng. Chọn **Overwrite existing library entries** khi bạn muốn thay thế các mục trùng trong thư viện.

## Cập nhật và đóng gói

Plugin chạy [easyeda2kicad của uPesy](https://github.com/uPesy/easyeda2kicad.py) từ [PyPI](https://pypi.org/project/easyeda2kicad/). Phiên bản hiện tại được ghim trong `plugins/requirements.txt` để mọi máy dùng cùng phiên bản engine. Upstream phát hành mã nguồn theo AGPL-3.0.

Khi upstream phát hành bản mới, sửa phiên bản trong `plugins/requirements.txt`, tăng phiên bản plugin trong `metadata.json` và thử nhập một linh kiện có model 3D. Phần liên kết model đọc đường dẫn footprint từ log của upstream, nên kiểm tra cả đường dẫn `MARUYAMA_3D` khi nâng cấp.

Chạy lệnh sau ở thư mục repo để tạo ZIP cài đặt. Chỉ người đóng gói cần chạy lệnh này.

```powershell
python build.py
```

Đính kèm `dist/lcsc-importer-pcm.zip` vào GitHub Release. Đồng đội tải file ZIP đó và cài trực tiếp trong KiCad.
