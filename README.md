<div align="center">
  <img src="images/AWS_Cover.png"/>
  <h1>☁️ AWS Learning Journey</h1>
  <p>
    <b>Người thực hiện:</b> Tiết Vinh Phú<br>
    <i>"Hành trình từ Zero đến Hero với AWS Cloud & DevOps"</i>
  </p>
  
  <a href="https://www.facebook.com/XueYongFu"><img src="https://img.shields.io/badge/Facebook-%231877F2.svg?style=for-the-badge&logo=Facebook&logoColor=white" alt="Facebook"></a>
  <a href="https://www.linkedin.com/in/tiet-vinh-phu-609173155/"><img src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
</div>

<br> ## 🗂️ Danh sách bài lab (Laboratory Overview)

<!-- TABLE_START -->
| Bài Lab (Lab) | Chủ đề (Topics) | Trạng thái (Status) | Tài liệu (Resources) |
| :--- | :--- | :--- | :--- |
| **[1. Create new AWS account](./The%20First%20Cloud%20Journey/1.%20Create%20new%20AWS%20account)** | <ul><li><strong>Tạo tài khoản AWS miễn phí</strong> từ A-Z với 9 bước chi tiết, tránh bị charge tiền không mong muốn</li><li><strong>Quản lý tài khoản hiệu quả:</strong> Xem Account ID, cập nhật thông tin, tạo Account Alias cho URL đăng nhập dễ nhớ</li><li><strong>Áp dụng Best Practices 2025:</strong> Bảo vệ Root User bằng MFA, thiết lập Billing Alert, và các nguyên tắc bảo mật quan trọng</li></ul> | ![Done](https://img.shields.io/badge/Status-Completed-success?style=flat-square) | [![Youtube](https://img.shields.io/badge/View-Video-red?style=flat-square&logo=youtube)](https://youtu.be/fDhiEsKYiHY?si=yZZ5VQNW20uOWTCn) |
| **[2. MFA for AWS Accounts](./The%20First%20Cloud%20Journey/2.%20MFA%20for%20AWS%20Accounts)** | <ul><li><strong>MFA (Multi-Factor Authentication)</strong> là lớp bảo mật thiết yếu nhất, yêu cầu 2 yếu tố xác thực: mật khẩu (something you know) + mã từ thiết bị MFA (something you have).</li><li><strong>Virtual MFA Device</strong> (Google Authenticator, Authy) tạo mã TOTP 6 số, là giải pháp miễn phí và dễ triển khai nhất cho tài khoản AWS.</li><li><strong>Root User</strong> bắt buộc phải bật MFA ngay sau khi tạo tài khoản - đây là chốt chặn quan trọng nhất bảo vệ toàn bộ hạ tầng AWS.</li></ul> | ![Done](https://img.shields.io/badge/Status-Completed-success?style=flat-square) | [![Youtube](https://img.shields.io/badge/View-Video-red?style=flat-square&logo=youtube)](https://youtu.be/osjvuki5fu8?si=urdvuIveM4CJUw9l) |
| **[3. Cost Management with AWS Budgets](./The%20First%20Cloud%20Journey/3.%20Cost%20Management%20with%20AWS%20Budgets)** | <ul><li><strong>AWS Budgets</strong> là công cụ thiết lập ngân sách tùy chỉnh để theo dõi chi phí và mức sử dụng tài nguyên AWS, gửi cảnh báo khi vượt ngưỡng.</li><li>Hỗ trợ 2 loại chính: <strong>Cost Budget</strong> (theo dõi tiền $) và <strong>Usage Budget</strong> (theo dõi mức sử dụng như giờ chạy EC2).</li><li>Là công cụ <strong>giám sát và cảnh báo</strong>, KHÔNG tự động dừng tài nguyên - cần kết hợp IAM/SCP để kiểm soát.</li></ul> | ![Done](https://img.shields.io/badge/Status-Completed-success?style=flat-square) | [![Youtube](https://img.shields.io/badge/View-Video-red?style=flat-square&logo=youtube)](https://youtu.be/_3o1QjIhm10?si=292FTZIqex6woSB1) |
| **[4. AWS Identity and Access Management (IAM) Access Control](./The%20First%20Cloud%20Journey/4.%20AWS%20Identity%20and%20Access%20Management%20%28IAM%29%20Access%20Control)** | <ul><li>Thiết lập môi trường IAM chuẩn, <strong>không dùng Root User</strong> cho công việc hàng ngày</li><li>Hiểu và thực hành kỹ thuật <strong>Switch Role</strong> để bảo mật tối đa</li><li>Nắm vững nguyên tắc <strong>Least Privilege</strong> (Đặc quyền tối thiểu)</li><li><strong>Luồng chính:</strong></li><li>Tạo Admin Group & User ➔ Tạo Role quyền lực (AdminRole) ➔ Tạo User hạn chế (OperatorUser) ➔ Cấu hình cho OperatorUser “mượn quyền” AdminRole</li><li><strong>Key Takeaway:</strong> Luôn tuân thủ nguyên tắc Least Privilege và hạn chế dùng credential dài hạn.</li><li>---</li></ul> | ![In Progress](https://img.shields.io/badge/Status-In_Progress-yellow?style=flat-square) | _Updating..._ |
<!-- TABLE_END -->

---
### 📈 Thống kê
![Commits](https://img.shields.io/github/last-commit/tietvinhphu/AWS-Journey?style=for-the-badge&color=blue)

<!--
HUỚNG DẪN CẬP NHẬT TRẠNG THÁI & LINK:

1. Đổi trạng thái sang "Completed" (Xanh lá): 
   Thay badge màu vàng cũ bằng đoạn này:
   ![Done](https://img.shields.io/badge/Status-Completed-success?style=flat-square)

2. Thêm link video Youtube:
   Thay chữ "_Updating..._" bằng:
   [![Youtube](https://img.shields.io/badge/View-Video-red?style=flat-square&logo=youtube)](LINK_VIDEO_CUA_BAN)
-->
