var path = require("path");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  context: __dirname,
  entry: {
    uploadLessonResource: "./curriculum/static/js/uploadLessonResource.js",
    starRating: "./firstbyte/static/firstbyte/js/starRating.js",
    cardHoverShadow: './curriculum/static/js/cardHoverShadow.js'
  },
  output: {
    path: path.resolve("./firstbyte/static/firstbyte/webpack_bundles/"),
    filename: "[name]-[hash].js"
  },
  mode: "development",

  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },

  plugins: [new BundleTracker({ filename: "./webpack-stats.json" })]
};
