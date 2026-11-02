// No browser play: the game runs inside the downloaded app (desktop shells tag their user agent, Android is a WebView), plus local dev and tests.
if (!/VancouverViceApp|; wv\)/.test(navigator.userAgent) && !navigator.webdriver && !/^(localhost|127\.0\.0\.1)$/.test(location.hostname)) location.replace("./#download");
