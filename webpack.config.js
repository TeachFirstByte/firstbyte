var path = require('path');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: {
      uploadLessonResource: './static/firstbyte/js/uploadLessonResource.js',
  },
  output: {
      path: path.resolve('./static/firstbyte/webpack_bundles/'),
      filename: "[name]-[hash].js"
  },
  mode: 'development',

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      }
    ]
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ]
}