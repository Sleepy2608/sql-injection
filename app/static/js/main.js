// Core Application JS

// Toast Notification Manager
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span>${message}</span>
      <button onclick="this.parentElement.parentElement.remove()" style="background:none; border:none; color:#94a3b8; cursor:pointer; font-size:1.1rem; margin-left:10px;">&times;</button>
    </div>
  `;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 4500);
}

// Global 1-Click Database Reset
async function triggerDatabaseReset() {
  if (!confirm('Bạn có chắc chắn muốn khôi phục toàn bộ cơ sở dữ liệu SQLite Sandbox về trạng thái ban đầu?')) {
    return;
  }

  try {
    const res = await fetch('/api/reset-db', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message, 'success');
      setTimeout(() => window.location.reload(), 1200);
    } else {
      showToast(data.error || 'Có lỗi xảy ra khi reset.', 'danger');
    }
  } catch (err) {
    showToast('Lỗi kết nối tới máy chủ sandbox.', 'danger');
  }
}

// Global Event Listener for Payload Chips
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.payload-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetInputId = btn.dataset.targetInput || 'username-input';
      const payloadVal = btn.dataset.payload || btn.textContent.trim();
      const targetInput = document.getElementById(targetInputId);
      
      if (targetInput) {
        targetInput.value = payloadVal;
        targetInput.focus();
        showToast(`Đã áp dụng payload: "${payloadVal}"`, 'info');
      }
    });
  });
});

