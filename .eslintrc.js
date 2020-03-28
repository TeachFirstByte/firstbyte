module.exports = {
    extends: [
      'eslint:recommended',
      'plugin:vue/recommended',
    ],
    rules: {
        "no-unused-vars": ["error", {"args": "after-used", "argsIgnorePattern": "^_"}],
        "vue/html-indent": ["error", 4],
        "no-var": "error",
        "semi": ["error", "always"],
    }
}