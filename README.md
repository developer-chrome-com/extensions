# extensions

[![Build Status](https://travis-ci.org/developer-chrome-com/extensions.svg?branch=master)](https://travis-ci.org/developer-chrome-com/extensions)

> Replicate of https://developer.chrome.com/extensions

Since HTML in this repo adopts `path/to/url/index.html`, it will meet path resolving issue for those originally `path/to/url.html`. If you are redirected to 404 page, have a try to re-type url logically.

Example:

1. Click on `content scripts` at https://developer-chrome-com.github.io/extensions/getstarted/

    Now you are redirected to https://developer-chrome-com.github.io/content_scripts.html.

    Visit https://developer-chrome-com.github.io/extensions/content_scripts/ by adding `extensions` and removing trailing `.html`.

1. Click on `manifest` at https://developer-chrome-com.github.io/extensions/getstarted/

    Now you are redirected to https://developer-chrome-com.github.io/extensions/getstarted/extensions/manifest.
    
    Visit https://developer-chrome-com.github.io/extensions/manifest/ by removing `extensions/getstarted`.

1. Click on `manifest_version` at https://developer-chrome-com.github.io/extensions/manifest/

    Now you are redirected to https://developer-chrome-com.github.io/extensions/manifest/manifest/manifest_version.
    
    Visit https://developer-chrome-com.github.io/extensions/manifest/manifest_version/ by removing `manifest`.
