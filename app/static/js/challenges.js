// CTF Challenges Manager

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.btn-submit-flag').forEach(btn => {
    btn.addEventListener('click', async () => {
      const challengeId = btn.dataset.challengeId;
      const inputEl = document.getElementById(`flag-input-${challengeId}`);
      if (!inputEl) return;

      const flag = inputEl.value.trim();
      if (!flag) {
        showToast('Vui lòng nhập flag để nộp bài.', 'warning');
        return;
      }

      btn.disabled = true;
      try {
        const response = await fetch('/challenges/api/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ challenge_id: challengeId, flag: flag })
        });
        const data = await response.json();

        if (data.success) {
          showToast(data.message, 'success');
          // Update status badge
          const statusBadge = document.getElementById(`status-${challengeId}`);
          if (statusBadge) {
            statusBadge.className = 'badge badge-success';
            statusBadge.textContent = 'ĐÃ HOÀN THÀNH';
          }
          btn.style.display = 'none';
          inputEl.disabled = true;
        } else {
          showToast(data.message, 'danger');
        }
      } catch (err) {
        showToast('Lỗi khi nộp flag.', 'danger');
      } finally {
        btn.disabled = false;
      }
    });
  });

  // Toggle Hint buttons
  document.querySelectorAll('.btn-toggle-hint').forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.targetHint;
      const hintEl = document.getElementById(targetId);
      if (hintEl) {
        if (hintEl.style.display === 'none' || !hintEl.style.display) {
          hintEl.style.display = 'block';
          btn.textContent = 'Ẩn gợi ý';
        } else {
          hintEl.style.display = 'none';
          btn.textContent = 'Xem gợi ý';
        }
      }
    });
  });
});

