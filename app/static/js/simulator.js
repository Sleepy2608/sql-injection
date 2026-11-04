// Live Interactive Simulator Execution Helper

document.addEventListener('DOMContentLoaded', () => {
  // 1. Auth Lab Form Handler
  const authForm = document.getElementById('auth-form');
  if (authForm) {
    authForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const username = document.getElementById('username-input').value;
      const password = document.getElementById('password-input').value;
      const mode = document.querySelector('input[name="mode"]:checked')?.value || 'vulnerable';
      const submitBtn = authForm.querySelector('button[type="submit"]');

      if (submitBtn) submitBtn.disabled = true;

      try {
        const response = await fetch('/lab/auth', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ username, password, mode })
        });
        const data = await response.json();
        renderAuthResult(data);
      } catch (err) {
        showToast('Lỗi khi gửi yêu cầu mô phỏng.', 'danger');
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  // 2. Search Lab Form Handler
  const searchForm = document.getElementById('search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const query = document.getElementById('search-input').value;
      const mode = document.querySelector('input[name="mode"]:checked')?.value || 'vulnerable';
      const submitBtn = searchForm.querySelector('button[type="submit"]');

      if (submitBtn) submitBtn.disabled = true;

      try {
        const response = await fetch('/lab/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ query, mode })
        });
        const data = await response.json();
        renderSearchResult(data);
      } catch (err) {
        showToast('Lỗi khi gửi yêu cầu tìm kiếm.', 'danger');
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }

  // 3. Filter Lab Form Handler
  const filterForm = document.getElementById('filter-form');
  if (filterForm) {
    filterForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const username = document.getElementById('username-input').value;
      const password = document.getElementById('password-input').value;
      const mode = document.querySelector('input[name="mode"]:checked')?.value || 'naive';
      const submitBtn = filterForm.querySelector('button[type="submit"]');

      if (submitBtn) submitBtn.disabled = true;

      try {
        const response = await fetch('/lab/filter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ username, password, mode })
        });
        const data = await response.json();
        renderFilterResult(data);
      } catch (err) {
        showToast('Lỗi khi gửi yêu cầu kiểm tra bộ lọc.', 'danger');
      } finally {
        if (submitBtn) submitBtn.disabled = false;
      }
    });
  }
});

function renderAuthResult(data) {
  const container = document.getElementById('result-container');
  if (!container) return;

  let alertHtml = '';
  if (data.success) {
    alertHtml = `
      <div class="alert alert-success">
        <div>
          <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 0.25rem;">
            🔓 Đăng nhập thành công! ${data.inspector?.injected_syntax_detected ? '(SQL INJECTION EXPLOITED)' : ''}
          </div>
          <div>Xin chào: <strong>${data.user.full_name}</strong> (@${data.user.username}) | Vai trò: <span class="badge ${data.user.role === 'admin' ? 'badge-danger' : 'badge-info'}">${data.user.role}</span></div>
          ${data.user.secret_note ? `<div style="margin-top: 0.5rem; font-family: monospace; background: rgba(0,0,0,0.3); padding: 6px 10px; border-radius: 4px;">📝 Ghi chú bí mật: ${data.user.secret_note}</div>` : ''}
        </div>
      </div>
    `;
  } else if (data.sql_syntax_error) {
    alertHtml = `
      <div class="alert alert-warning">
        <div>
          <div style="font-weight: 700;">⚠️ Phát hiện lỗi cú pháp SQLite (Error-based Insight)</div>
          <div style="font-family: monospace; margin-top: 4px;">${data.error}</div>
        </div>
      </div>
    `;
  } else {
    alertHtml = `
      <div class="alert alert-danger">
        <div>
          <div style="font-weight: 700;">🔒 Đăng nhập thất bại</div>
          <div>${data.error || 'Xác thực không thành công.'}</div>
        </div>
      </div>
    `;
  }

  // Update Inspector
  const inspector = data.inspector;
  const inspectorHtml = renderInspectorHtml(inspector);

  container.innerHTML = alertHtml + inspectorHtml;
}

function renderSearchResult(data) {
  const container = document.getElementById('result-container');
  if (!container) return;

  let contentHtml = '';
  if (data.success) {
    const isExploited = data.inspector?.raw_query.toUpperCase().includes('UNION');
    let rowsHtml = '';
    
    if (data.results && data.results.length > 0) {
      const cols = data.columns || Object.keys(data.results[0]);
      const thead = cols.map(c => `<th>${c}</th>`).join('');
      const tbody = data.results.map(r => `
        <tr>${cols.map(c => `<td>${r[c] !== null && r[c] !== undefined ? r[c] : '<em>null</em>'}</td>`).join('')}</tr>
      `).join('');

      rowsHtml = `
        <div class="table-responsive" style="margin-top: 1rem;">
          <table class="data-table">
            <thead><tr>${thead}</tr></thead>
            <tbody>${tbody}</tbody>
          </table>
        </div>
      `;
    } else {
      rowsHtml = '<p style="color: var(--text-muted); margin-top: 1rem;">Không tìm thấy sản phẩm nào khớp với từ khóa.</p>';
    }

    contentHtml = `
      <div class="alert ${isExploited ? 'alert-danger' : 'alert-info'}">
        <div>
          <div style="font-weight: 700;">
            ${isExploited ? '🚨 DỮ LIỆU BỊ RÒ RỈ THÀNH CÔNG QUA MỆNH ĐỀ UNION SELECT!' : '🔍 Kết quả tìm kiếm'}
          </div>
          <div>Tìm thấy <strong>${data.count}</strong> bản ghi trả về từ cơ sở dữ liệu.</div>
        </div>
      </div>
      ${rowsHtml}
    `;
  } else {
    contentHtml = `
      <div class="alert alert-warning">
        <div>
          <div style="font-weight: 700;">⚠️ Lỗi thực thi truy vấn SQLite</div>
          <div style="font-family: monospace; margin-top: 4px;">${data.error}</div>
        </div>
      </div>
    `;
  }

  const inspector = data.inspector;
  const inspectorHtml = renderInspectorHtml(inspector);

  container.innerHTML = contentHtml + inspectorHtml;
}

function renderFilterResult(data) {
  const container = document.getElementById('result-container');
  if (!container) return;

  let alertHtml = '';
  if (data.blocked_by_filter) {
    alertHtml = `
      <div class="alert alert-danger">
        <div>
          <div style="font-weight: 700;">🛡️ Bị chặn bởi bộ lọc WAF / Naive Blacklist</div>
          <div>${data.filter_reason}</div>
        </div>
      </div>
    `;
  } else if (data.bypassed_filter && data.success) {
    alertHtml = `
      <div class="alert alert-success">
        <div>
          <div style="font-weight: 700;">🎯 VƯỢT QUA BỘ LỌC THÀNH CÔNG (BYPASS EXPLOITED)!</div>
          <div>${data.filter_reason}</div>
          <div style="margin-top: 0.5rem;">Đăng nhập thành công tài khoản: <strong>${data.user?.full_name}</strong> (@${data.user?.username})</div>
        </div>
      </div>
    `;
  } else if (data.success) {
    alertHtml = `
      <div class="alert alert-success">
        <div>
          <div style="font-weight: 700;">🔓 Đăng nhập thành công</div>
          <div>Tài khoản: <strong>${data.user?.full_name}</strong></div>
        </div>
      </div>
    `;
  } else {
    alertHtml = `
      <div class="alert alert-warning">
        <div>
          <div style="font-weight: 700;">🔒 Đăng nhập thất bại</div>
          <div>${data.error}</div>
        </div>
      </div>
    `;
  }

  const inspector = data.inspector;
  const inspectorHtml = renderInspectorHtml(inspector);

  container.innerHTML = alertHtml + inspectorHtml;
}

function renderInspectorHtml(inspector) {
  if (!inspector) return '';
  return `
    <div class="inspector-card">
      <div class="inspector-header">
        <span class="inspector-title">⚡ LIVE SQL QUERY INSPECTOR</span>
        <span class="badge ${inspector.mode === 'secure' ? 'badge-success' : 'badge-danger'}">${inspector.mode}</span>
      </div>
      <div class="inspector-body">
        <div class="sql-terminal">${inspector.html_output}</div>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-top: 0.5rem; line-height: 1.6;">
          ${inspector.explanation}
        </p>
        <div style="margin-top: 0.5rem; font-family: monospace; font-size: 0.8rem; color: #64748b;">
          ${inspector.params_display}
        </div>
        <div class="inspector-legend">
          <div class="legend-item"><div class="legend-swatch" style="background: #94a3b8;"></div> Code gốc</div>
          <div class="legend-item"><div class="legend-swatch" style="background: #ff3366;"></div> Payload tiêm nhiễm</div>
          <div class="legend-item"><div class="legend-swatch" style="background: #ffaa00;"></div> Ký hiệu Comment</div>
          <div class="legend-item"><div class="legend-swatch" style="background: #475569;"></div> Code bị vô hiệu</div>
          <div class="legend-item"><div class="legend-swatch" style="background: #00e676;"></div> Tham số an toàn (?)</div>
        </div>
      </div>
    </div>
  `;
}

