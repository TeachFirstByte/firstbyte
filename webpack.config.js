var path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  context: __dirname,
  entry: {
    uploadLessonResource: "./curriculum/static/js/uploadLessonResource.js",
    starRating: "./firstbyte/static/firstbyte/js/starRating.js",
    cardHoverShadow: './curriculum/static/js/cardHoverShadow.js',
    loanerProgram: './loaner_program/static/loaner_program/js/app.js',
  },
  output: {
    path: path.resolve("./firstbyte/static/firstbyte/webpack_bundles/"),
    filename: "[name]-[hash].js"
  },
  mode: "development",
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js'
    }
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      }
    ]
  },

  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new VueLoaderPlugin()
  ]
};
