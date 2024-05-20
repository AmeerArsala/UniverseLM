/** @type { import("eslint").Linter.Config } */
module.exports = {
    root: true,
    extends: ["eslint:recommended", "plugin:svelte/recommended", "prettier", "plugin:astro/recommended", "plugin:tailwindcss/recommended", "plugin:react/recommended"],
    plugins: ["svelte4"],
    parserOptions: {
      sourceType: "module",
      ecmaVersion: 2020,
      extraFileExtensions: [".svelte", ".astro", ".tsx", ".jsx"],
    },
    rules: {
      "no-cond-assign": "warn",
      "no-constant-condition": "warn",
      "no-unreachable": "warn",
      "no-unused-expressions": "warn",
      "no-constant-binary-expression": "warn",
      "no-sequences": "warn",
    },
    env: {
      browser: true,
      es2017: true,
      node: true,
    },
  };
