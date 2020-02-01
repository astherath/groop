'use strict';

var React = require("react");

function Title(Props) {
  var title = Props.title;
  return React.createElement("div", undefined, React.createElement("h1", undefined, title));
}

var make = Title;

exports.make = make;
/* react Not a pure module */
