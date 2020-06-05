/* eslint-disable */
var path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  context: __dirname,
  devtool: 'source-map',
  entry: {
    firstByteBootstrap: "./firstbyte/static/firstbyte/js/bootstrap.js",
    starRating: "./firstbyte/static/firstbyte/js/starRating.js",
    cardHoverShadow: './curriculum/static/js/cardHoverShadow.js',
    loanerProgram: './loaner_program/static/loaner_program/js/app.js',
    curriculumForm: './curriculum/static/js/curriculumForm.js'
  },
  output: {
    path: path.resolve("./firstbyte/static/firstbyte/webpack_bundles/"),
    filename: "[name]-[hash].js"
  },
  mode: "development",
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    }
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/,
        use: [
          'file-loader',
        ],
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.s[ac]ss$/,
        use: [{
          loader: 'style-loader', // inject CSS to page
        }, {
          loader: 'css-loader', // translates CSS into CommonJS modules
        }, {
          loader: 'postcss-loader', // Run post css actions
          options: {
            plugins: function () { // post css plugins, can be exported to postcss.config.js
              return [
                require('precss'),
                require('autoprefixer')
              ];
            }
          }
        }, {
          loader: 'sass-loader' // compiles Sass to CSS
        }]
      },
    ],
  },
  plugins: [
    new BundleTracker({ filename: "./webpack-stats.json" }),
    new VueLoaderPlugin()
  ],
};
