# Cài profile “Engineering & Algorithms”

Thiết kế riêng cho **Nguyen Bao Toan / toan149**, **sinh viên năm 3 Đại học FPT**. Profile thể hiện cả **Software Engineering** và **Competitive Programming**: phần ứng dụng, dữ liệu và công cụ được đặt trước phần thuật toán/Codeforces. Banner GIF giữ góc máy tính Ubuntu, C++17, con trỏ nhấp nháy, bàn phím, chuột và cà phê chuyển động.

## Đăng lên GitHub

1. Đăng nhập tài khoản **NgBaoToan**. Tạo repository **Public** có tên chính xác **NgBaoToan** tại https://github.com/new. Đây là tên GitHub cần để hiện README trên trang cá nhân.
2. Giải nén gói này. Đưa **nội dung bên trong** thư mục `NgBaoToan-profile` lên thư mục gốc của repo: `README.md`, `assets/`, `data/`, `scripts/` và `.github/`. Đừng đưa nguyên thư mục cha lên repo.
3. Commit rồi mở https://github.com/NgBaoToan để xem profile. Banner và mọi liên hệ hoạt động ngay; không cần key riêng cho Codeforces.
4. Để bật cập nhật số liệu: mở tab **Actions → Refresh Codeforces profile → Run workflow** và chạy một lần. Workflow dự kiến chạy mỗi ngày lúc **07:17 và 19:17 giờ Việt Nam**; GitHub có thể chạy trễ. Workflow cần nằm trên nhánh mặc định.

Nếu dùng terminal Ubuntu, sau khi tạo repo **trống** trên GitHub, mở terminal trong thư mục `NgBaoToan-profile` đã giải nén rồi chạy:

```bash
git init -b main
git add README.md assets data scripts .github
git commit -m "feat: add Engineering & Algorithms profile"
git remote add origin https://github.com/NgBaoToan/NgBaoToan.git
git push -u origin main
```

Các lệnh này dành cho thư mục mới giải nén và repo mới chưa có commit. Nếu tải bằng giao diện web, nhớ đưa cả thư mục ẩn `.github` lên để có workflow cập nhật. `preview.html`, `profile-preview.png`, `SETUP.md` và `DESIGN.md` là tài liệu đi kèm, không bắt buộc phải đăng.

**Lưu ý khi dùng trình quản lý tệp:** `.github` là thư mục ẩn trên Ubuntu. Nhấn `Ctrl+H` để thấy nó. Nếu kéo thả trên web bỏ sót thư mục này, dùng Git theo cách dưới đây.

### Đưa lên bằng Git trên Ubuntu

Sau khi tạo repo trống trên GitHub, mở terminal trong thư mục `NgBaoToan-profile` rồi chạy:

```bash
git init
git branch -M main
git add README.md assets data scripts .github SETUP.md DESIGN.md
git commit -m "feat: add Engineering & Algorithms profile"
git remote add origin https://github.com/NgBaoToan/NgBaoToan.git
git push -u origin main
```

Nếu repo đã có nội dung, hãy clone repo rồi chép các tệp này vào bản clone và commit bình thường. Không cần force push. GitHub sẽ yêu cầu đăng nhập nếu máy chưa được xác thực.

## Thông tin liên hệ đã điền

| Nền tảng | Địa chỉ |
| --- | --- |
| Codeforces | https://codeforces.com/profile/toan149 |
| Email | toannb149@gmail.com |
| Facebook | https://www.facebook.com/ngbaotoan1204/ |
| Instagram | https://www.instagram.com/_nberton._/ |

## Cơ chế số liệu

- `scripts/update_codeforces.py` lấy rating, best rating, số cuộc thi rated và lịch sử rating từ API công khai của Codeforces. Dữ liệu hiển thị là **snapshot có thời điểm cập nhật**, không phải stream thời gian thực.
- Chỉ dùng thư viện chuẩn Python 3. Không cần cài package hoặc dùng Codeforces API key.
- Khi API lỗi, giữ dữ liệu tốt gần nhất và thời điểm cũ; không thay thành số 0. Nếu chưa từng đồng bộ, hiện trạng thái chờ thay vì tạo số liệu giả.
- `assets/codeforces-live.svg` nằm trong repo, tránh phụ thuộc dịch vụ tạo badge bên thứ ba. GitHub vẫn có thể cache ảnh một thời gian sau khi cập nhật.
- Nếu Actions báo không có quyền push, xem **Settings → Actions → General → Workflow permissions**. Repo cần cho phép workflow ghi nội dung; branch protection cũng có thể chặn commit trực tiếp.
- GitHub có thể tạm ngưng workflow theo lịch trên repo công khai lâu không có hoạt động. Khi cần, bật lại trong Actions.

Chạy thủ công trên máy:

```bash
python3 scripts/update_codeforces.py
```

Chỉ dựng lại ảnh từ dữ liệu đang lưu:

```bash
python3 scripts/update_codeforces.py --offline
```

## Chỉnh nội dung

- Giới thiệu, các liên kết: `README.md`.
- Thay thông tin trên nút liên hệ: sửa thêm chữ trong `assets/email.svg`, `assets/facebook.svg`, `assets/instagram.svg`; liên kết đích nằm trong README.
- Thay ảnh banner: `assets/hero.gif`; bản vector tĩnh có trong `assets/hero-static.svg`. Có thể dựng lại GIF bằng `python3 scripts/build_hero_gif.py` (cần Inkscape và Pillow).
- `preview.html` là bản xem trước cục bộ với nội dung README. Mở nó bằng trình duyệt; bố cục thực tế trên GitHub có thể khác nhẹ do giao diện GitHub.
- `profile-preview.png` là ảnh xem trước toàn bộ profile để kiểm tra nhanh.

Nguồn hướng dẫn: [Profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [GitHub Actions schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [Workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions), [Codeforces API](https://codeforces.com/apiHelp/methods).

Để dựng lại các tài sản SVG từ mã nguồn, chạy `python3 scripts/build_assets.py`. Script này không sửa README. Bản GIF đã có sẵn trong gói.
