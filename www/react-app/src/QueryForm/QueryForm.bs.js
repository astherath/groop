'use strict';

var Block = require("bs-platform/lib/js/block.js");
var Curry = require("bs-platform/lib/js/curry.js");
var React = require("react");
var Formality__Form = require("re-formality/src/Formality__Form.bs.js");
var Formality__PublicHelpers = require("re-formality/src/Formality__PublicHelpers.bs.js");

function update(state, value) {
  return {
          query: value
        };
}

function validator_validate(state) {
  var match = state.query;
  if (match === "") {
    return /* Error */Block.__(1, ["Invalid Query"]);
  } else {
    return /* Ok */Block.__(0, [/* Valid */0]);
  }
}

var validator = {
  field: /* Query */0,
  strategy: /* OnFirstSuccessOrFirstBlur */3,
  dependents: undefined,
  validate: validator_validate
};

var QueryField = {
  update: update,
  validator: validator
};

var validators = /* :: */[
  validator,
  /* [] */0
];

var QueryForm = {
  QueryField: QueryField,
  validators: validators
};

var QueryFormHook = Formality__Form.Make({
      validators: validators
    });

function QueryForm$1(Props) {
  var form = Curry._2(QueryFormHook.useForm, {
        query: ""
      }, (function (state, form) {
          console.log("inputted this" + state.query);
          return /* () */0;
        }));
  var partial_arg = form.submit;
  var match = Curry._1(form.result, /* Query */0);
  var tmp;
  if (match !== undefined) {
    var match$1 = match;
    tmp = match$1.tag ? React.createElement("div", {
            className: "failure"
          }, match$1[0]) : null;
  } else {
    tmp = null;
  }
  var match$2 = form.submitting;
  return React.createElement("form", {
              onSubmit: (function (param) {
                  return Formality__PublicHelpers.Dom.preventDefault(partial_arg, param);
                })
            }, React.createElement("input", {
                  disabled: form.submitting,
                  value: form.state.query,
                  onBlur: (function (param) {
                      return Curry._1(form.blur, /* Query */0);
                    }),
                  onChange: (function ($$event) {
                      return Curry._2(form.change, /* Query */0, (form.state, {
                                    query: $$event.target.value
                                  }));
                    })
                }), tmp, React.createElement("div", {
                  style: {
                    height: "10px"
                  }
                }), React.createElement("button", {
                  style: {
                    color: "blue",
                    height: "50px",
                    width: "80px"
                  },
                  disabled: form.submitting
                }, match$2 ? "Submitting..." : "Submit"));
}

var make = QueryForm$1;

exports.QueryForm = QueryForm;
exports.QueryFormHook = QueryFormHook;
exports.make = make;
/* QueryFormHook Not a pure module */
