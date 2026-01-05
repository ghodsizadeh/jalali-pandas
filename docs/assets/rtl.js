(() => {
  const path = window.location.pathname || "";
  const is_fa =
    path.includes("/fa/") || path.endsWith("/fa") || path.endsWith("/fa/");

  const html = document.documentElement;
  const body = document.body;

  if (is_fa) {
    html.lang = "fa";
    html.dir = "rtl";
    if (body) {
      body.dir = "rtl";
    }
  } else {
    html.lang = "en";
    html.dir = "ltr";
    if (body) {
      body.dir = "ltr";
    }
  }
})();
