(() => {
  const THEME_KEY = "olexa_theme";
  const CART_KEY = "olexa_rabbit_cart";

  const $ = (id) => document.getElementById(id);

  const yearEl = $("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  const root = document.documentElement;
  const getInitialTheme = () => {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "light" || saved === "dark") return saved;
    const prefersDark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    return prefersDark ? "dark" : "light";
  };

  const applyTheme = (theme) => {
    if (theme === "dark") {
      root.setAttribute("data-theme", "dark");
    } else {
      root.removeAttribute("data-theme");
      theme = "light";
    }
    localStorage.setItem(THEME_KEY, theme);
    const icon = $("themeIcon");
    if (icon) icon.textContent = theme === "dark" ? "☀" : "🌙";
  };

  applyTheme(getInitialTheme());

  const products = [
    {
      id: "dwarf",
      name: "Карликовий кролик",
      tag: "Домашній",
      price: 1200,
      meta: ["Вага: 0.9–1.6 кг", "Характер: лагідний", "Догляд: середній"],
    },
    {
      id: "lop",
      name: "Вухань (Lop)",
      tag: "Популярний",
      price: 1600,
      meta: ["Вага: 1.4–2.2 кг", "Вуха: висячі", "Догляд: простий"],
    },
    {
      id: "rex",
      name: "Рекс",
      tag: "Плюшевий",
      price: 1800,
      meta: ["Шерсть: оксамит", "Характер: спокійний", "Догляд: простий"],
    },
    {
      id: "lionhead",
      name: "Левоголовий",
      tag: "Краса",
      price: 2000,
      meta: ["Грива: так", "Линька: помірна", "Догляд: уважний"],
    },
    {
      id: "giant",
      name: "Фландр (велетень)",
      tag: "Великий",
      price: 3500,
      meta: ["Вага: 5–8 кг", "Місце: більше", "Догляд: середній"],
    },
    {
      id: "californian",
      name: "Каліфорнійський",
      tag: "Фермерський",
      price: 2200,
      meta: ["Вага: 3.5–4.8 кг", "Витривалий", "Догляд: простий"],
    },
  ];

  const formatUAH = (value) =>
    new Intl.NumberFormat("uk-UA", {
      style: "currency",
      currency: "UAH",
      maximumFractionDigits: 0,
    }).format(value);

  const loadCart = () => {
    try {
      const raw = localStorage.getItem(CART_KEY);
      const parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  };

  const saveCart = (cart) => {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
  };

  const addToCart = (productId) => {
    const cart = loadCart();
    cart.push({ productId, ts: Date.now() });
    saveCart(cart);
  };

  const removeFromCart = (index) => {
    const cart = loadCart();
    cart.splice(index, 1);
    saveCart(cart);
  };

  const clearCart = () => {
    saveCart([]);
  };

  const cartModal = $("cartModal");
  const cartList = $("cartList");
  const cartEmpty = $("cartEmpty");
  const cartCount = $("cartCount");

  const openCart = () => {
    if (!cartModal) return;
    cartModal.hidden = false;
    renderCart();
    document.body.style.overflow = "hidden";
  };

  const closeCart = () => {
    if (!cartModal) return;
    cartModal.hidden = true;
    document.body.style.overflow = "";
  };

  const renderCart = () => {
    const cart = loadCart();
    if (cartCount) cartCount.textContent = String(cart.length);
    if (!cartList || !cartEmpty) return;

    if (cart.length === 0) {
      cartList.innerHTML = "";
      cartEmpty.style.display = "block";
      return;
    }

    cartEmpty.style.display = "none";

    const items = cart
      .map((item, idx) => {
        const product = products.find((p) => p.id === item.productId);
        const title = product ? product.name : "Товар";
        const price = product ? formatUAH(product.price) : "";
        return `
          <div class="cart-item" data-cart-index="${idx}">
            <div class="cart-item-row">
              <div class="cart-item-title">${title}</div>
              <div class="cart-item-price">${price}</div>
            </div>
            <div class="cart-item-actions">
              <button class="btn btn-ghost btn-small" type="button" data-remove="${idx}">
                Видалити
              </button>
            </div>
          </div>
        `;
      })
      .join("");

    cartList.innerHTML = items;
  };

  renderCart();

  const cartOpen = $("cartOpen");
  if (cartOpen) cartOpen.addEventListener("click", openCart);

  const trackOrderBtn = $("trackOrder");
  if (trackOrderBtn) {
    trackOrderBtn.addEventListener("click", () => {
      const id = window.prompt("Введи номер замовлення (демо):");
      if (!id) return;
      window.alert(`Поки що це демо. Замовлення №${id} шукаємо в системі :)`);
    });
  }

  const themeToggle = $("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  const enablePageTransitions = () => {
    document.body.classList.add("page-enter");
    const links = Array.from(
      document.querySelectorAll('a[href$=".html"]:not([target="_blank"])')
    );
    links.forEach((link) => {
      link.addEventListener("click", (e) => {
        if (!(link instanceof HTMLAnchorElement)) return;
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        const url = new URL(link.href, window.location.href);
        if (url.origin !== window.location.origin) return;
        e.preventDefault();
        const currentPath = window.location.pathname;
        const direction = url.pathname > currentPath ? "right" : "left";
        document.body.classList.add(
          direction === "right" ? "page-exit-right" : "page-exit-left"
        );
        setTimeout(() => {
          window.location.href = url.toString();
        }, 220);
      });
    });
  };

  enablePageTransitions();

  const cartClear = $("cartClear");
  if (cartClear) {
    cartClear.addEventListener("click", () => {
      clearCart();
      renderCart();
    });
  }

  if (cartModal) {
    cartModal.addEventListener("click", (e) => {
      const target = e.target;
      if (!(target instanceof HTMLElement)) return;

      if (target.getAttribute("data-close") === "cart") {
        closeCart();
        return;
      }

      const removeIdxRaw = target.getAttribute("data-remove");
      if (removeIdxRaw) {
        const idx = Number(removeIdxRaw);
        if (Number.isFinite(idx)) {
          removeFromCart(idx);
          renderCart();
        }
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !cartModal.hidden) closeCart();
    });
  }

  const catalogGrid = $("catalogGrid");
  const searchInput = $("searchInput");
  const filterChips = $("filterChips");

  const renderCatalog = (query = "", tagFilter = "all") => {
    if (!catalogGrid) return;
    const q = query.toLowerCase();
    const items = products.filter((p) => {
      const matchesTag = tagFilter === "all" || p.tag === tagFilter;
      const text = (p.name + " " + p.tag + " " + p.meta.join(" ")).toLowerCase();
      const matchesSearch = !q || text.includes(q);
      return matchesTag && matchesSearch;
    });

    catalogGrid.innerHTML = items
      .map((p) => {
        const meta = p.meta.map((m) => `<li>${m}</li>`).join("");
        return `
          <article class="product" data-product-id="${p.id}">
            <div class="product-top">
              <span class="badge">${p.tag}</span>
              <h3 class="product-title">${p.name}</h3>
              <div class="product-price">${formatUAH(p.price)}</div>
            </div>
            <ul class="product-meta">${meta}</ul>
            <div class="product-actions">
              <button class="btn btn-primary" type="button" data-buy="${p.id}">
                Купити
              </button>
              <button class="btn btn-ghost" type="button" data-ask="${p.id}">
                Запитати
              </button>
            </div>
          </article>
        `;
      })
      .join("");
  };

  if (catalogGrid) {
    let currentTag = "all";
    let currentQuery = "";
    renderCatalog();

    catalogGrid.addEventListener("click", (e) => {
      const target = e.target;
      if (!(target instanceof HTMLElement)) return;

      const buyId = target.getAttribute("data-buy");
      const askId = target.getAttribute("data-ask");

      if (buyId) {
        addToCart(buyId);
        renderCart();
        openCart();
      }

      if (askId) {
        const product = products.find((p) => p.id === askId);
        const name = product ? product.name : "породі";
        const url = new URL("./contact.html", window.location.href);
        url.searchParams.set("topic", name);
        window.location.href = url.toString();
      }
    });

    if (searchInput) {
      searchInput.addEventListener("input", () => {
        currentQuery = searchInput.value;
        renderCatalog(currentQuery, currentTag);
      });
    }

    if (filterChips) {
      filterChips.addEventListener("click", (e) => {
        const target = e.target;
        if (!(target instanceof HTMLElement)) return;
        const btn = target.closest("[data-filter]");
        if (!(btn instanceof HTMLElement)) return;
        currentTag = btn.getAttribute("data-filter") || "all";
        Array.from(filterChips.querySelectorAll("[data-filter]")).forEach((el) => {
          el.setAttribute("data-active", el === btn ? "true" : "false");
        });
        renderCatalog(currentQuery, currentTag);
      });
    }
  }

  const backToTop = $("backToTop");
  if (backToTop) {
    backToTop.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  document.addEventListener("click", (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;
    const link = target.closest('a[href^="#"]');
    if (!(link instanceof HTMLAnchorElement)) return;
    const href = link.getAttribute("href");
    if (!href || href === "#") return;
    const id = href.slice(1);
    const el = document.getElementById(id);
    if (!el) return;
    e.preventDefault();
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  const form = $("contactForm");
  const hint = $("formHint");
  if (form && hint) {
    const topic = new URLSearchParams(window.location.search).get("topic");
    if (topic) {
      const msg = form.querySelector('textarea[name="message"]');
      if (msg instanceof HTMLTextAreaElement) {
        msg.value = msg.value.trim()
          ? `${msg.value.trim()}\nПитання по: ${topic}.`
          : `Питання по: ${topic}.`;
      }
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("name") ?? "").trim();
      const email = String(data.get("email") ?? "").trim();
      const message = String(data.get("message") ?? "").trim();

      if (!name || !email || !message) {
        hint.textContent = "Заповни всі поля, будь ласка.";
        return;
      }

      const cart = loadCart();
      clearCart();
      renderCart();
      hint.textContent =
        cart.length > 0
          ? "Заявку збережено (демо). Ми зв’яжемось з тобою для підтвердження."
          : "Готово! (Це демо — відправку на сервер ще не підключено.)";
      form.reset();
    });
  }
})();
