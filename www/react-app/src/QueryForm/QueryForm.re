module QueryForm = {
	open Formality;

	// naming fields in form
	type field = Query;

	// setting state for value retrieval later
	type state = {
		query: string
	};

	// type of message that form can return
	type message = string;

	// list types of submission errors (planned and unplanned)
	type submissionError = UnexpectedServerError;

	// field validators
	module QueryField = {
		// set update calls for later
		let update = (state, value) => {...state, query: value};
		// validators use strategy to set and check fields + states
		let validator = {
			field: Query,
			strategy: Strategy.OnFirstSuccessOrFirstBlur,
			dependents: None,
			validate: state =>
				switch (state.query) {
					// pattern match for empty input
					| "" => Error("Invalid Query")
					| _ => Ok(Valid)
					},
		};
	};

	let validators = [QueryField.validator,];
};

// hook for the query form
module QueryFormHook = Formality.Make(QueryForm);

[@react.component]
let make = () => {
	let form =
		QueryFormHook.useForm(
			~initialState={query: ""},
			~onSubmit=(state, form) => {
				Js.log("inputted this") //XXX put in query string here
			},
		);
	// now form the actual jsx form
	<form onSubmit={form.submit->Formality.Dom.preventDefault}>
		<input
		value={form.state.query}
		disabled={form.submitting}
		onBlur={_ => form.blur(Query)}
		onChange={event =>
			form.change(
				Query,
				QueryForm.QueryField.update(
					form.state,
					event->ReactEvent.Form.target##value,
				),
			)
		}
		/>
		{switch (Query->(form.result)) {
			| Some(Error(message)) =>
			<div className="failure"> message->React.string </div>
			| Some(Ok(Valid | NoValue))
			| None => React.null
			}}
		<button disabled={form.submitting}>
			(form.submitting ? "Submitting..." : "Submit") -> React.string
		</button>
	</form>;
};
