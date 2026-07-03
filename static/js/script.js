// =========================================================
// PASTORÃO — Mini Mercado de Bairro
// Interatividade do front-end (sem dependências externas)
// =========================================================

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initQtySteppers();
  initFlashAutoHide();
  initTableSearch();
  initRemoveConfirm();
});

/* ---------- Menu mobile ---------- */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
}

/* ---------- Contador de quantidade (detalhe do produto / carrinho) ---------- */
function initQtySteppers() {
  document.querySelectorAll('.qty-stepper').forEach((stepper) => {
    const input = stepper.querySelector('input');
    const minus = stepper.querySelector('.qty-minus');
    const plus = stepper.querySelector('.qty-plus');
    if (!input) return;

    const min = parseInt(input.min || '1', 10);
    const max = parseInt(input.max || '99', 10);

    const clamp = (value) => Math.min(max, Math.max(min, value));

    minus?.addEventListener('click', () => {
      input.value = clamp((parseInt(input.value, 10) || min) - 1);
      input.dispatchEvent(new Event('change'));
    });

    plus?.addEventListener('click', () => {
      input.value = clamp((parseInt(input.value, 10) || min) + 1);
      input.dispatchEvent(new Event('change'));
    });

    input.addEventListener('change', () => {
      const value = parseInt(input.value, 10);
      input.value = clamp(Number.isNaN(value) ? min : value);
    });
  });
}

/* ---------- Mensagens flash desaparecem sozinhas ---------- */
function initFlashAutoHide() {
  document.querySelectorAll('.flash').forEach((flash) => {
    setTimeout(() => {
      flash.style.transition = 'opacity .4s ease';
      flash.style.opacity = '0';
      setTimeout(() => flash.remove(), 400);
    }, 5000);
  });
}

/* ---------- Busca instantânea em tabelas (admin) ---------- */
function initTableSearch() {
  document.querySelectorAll('[data-table-search]').forEach((input) => {
    const tableId = input.getAttribute('data-table-search');
    const table = document.getElementById(tableId);
    if (!table) return;

    input.addEventListener('input', () => {
      const term = input.value.trim().toLowerCase();
      table.querySelectorAll('tbody tr').forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  });
}

/* ---------- Confirmação antes de remover (carrinho/admin) ---------- */
function initRemoveConfirm() {
  document.querySelectorAll('[data-confirm]').forEach((el) => {
    el.addEventListener('click', (event) => {
      const message = el.getAttribute('data-confirm') || 'Tem certeza?';
      if (!window.confirm(message)) {
        event.preventDefault();
      }
    });
  });
}
