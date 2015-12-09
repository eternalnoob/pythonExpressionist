path =require('path')
module.exports = {
  entry: path.resolve(__dirname, 'static/scripts/jsx/main.jsx'),
  output: {
    path: path.resolve(__dirname, 'static/scripts/build'),
    filename: 'bundle.js'
  },
  module: {
    loaders: [{
      test: /\.jsx?$/, // A regexp to test the require path. accepts either js or jsx
      loader: 'babel' // The module to load. "babel" is short for "babel-loader"
    }]
  }
};

