'use strict';

;( function ( document, window, index )
{
    var url = "https://groop.pw:3000/files/upload";
    var errorAlert = document.getElementById("error-alert");
    var filename = "";
    var error = false;
    var droppedHandle = false;
    
    // message functions for error alert
    var displayError = function (errorMessage)
    {
        errorAlert.style = "display: content;";
        errorAlert.innerHTML = errorMessage;
    }
    var hideError = function()
    {
        errorAlert.style = "display: none;";
        errorAlert.innerHTML = "";
    }
    
    // feature detection for drag&drop upload
    var isAdvancedUpload = function()
        {
            var div = document.createElement( 'div' );
            return ( ( 'draggable' in div ) || ( 'ondragstart' in div && 'ondrop' in div ) ) && 'FormData' in window && 'FileReader' in window;
        }();


    // applying the effect for every form
    var forms = document.querySelectorAll( '.box' );
    Array.prototype.forEach.call( forms, function( form )
    {
        var input		 = form.querySelector( 'input[type="file"]' ),
            label		 = form.querySelector( 'label' ),
            errorMsg	 = form.querySelector( '.box__error' ),
            restart		 = form.querySelectorAll( '.box__restart' ),
            droppedFiles = false,
            showFiles	 = function( files )
            {
                filename = files[0].name;
                label.textContent = files[0].name;
            },
            triggerFormSubmit = function()
            {
                var event = document.createEvent( 'HTMLEvents' );
                event.initEvent( 'submit', true, false );
                form.dispatchEvent( event );
            };

        // letting the server side to know we are going to make an Ajax request
        var ajaxFlag = document.createElement( 'input' );
        ajaxFlag.setAttribute( 'type', 'hidden' );
        ajaxFlag.setAttribute( 'name', 'ajax' );
        ajaxFlag.setAttribute( 'value', 1 );
        form.appendChild( ajaxFlag );

        // automatically submit the form on file select
        input.addEventListener( 'change', function( e )
        {
            showFiles(e.target.files);
        });

        // drag&drop files if the feature is available
        if( isAdvancedUpload )
        {
            form.classList.add( 'has-advanced-upload' ); // letting the CSS part to know drag&drop is supported by the browser

            [ 'drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop' ].forEach( function( event )
            {
                form.addEventListener( event, function( e )
                {
                    // preventing the unwanted behaviours
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
            [ 'dragover', 'dragenter' ].forEach( function( event )
            {
                form.addEventListener( event, function()
                {
                    form.classList.add( 'is-dragover' );
                });
            });
            [ 'dragleave', 'dragend', 'drop' ].forEach( function( event )
            {
                form.addEventListener( event, function()
                {
                    form.classList.remove( 'is-dragover' );
                });
            });
            form.addEventListener( 'drop', function( e )
            {
                droppedHandle = true;
                droppedFiles = e.dataTransfer.files; // the files that were dropped
                showFiles( droppedFiles );

                                });
        }
        


        // if the form was submitted
        form.addEventListener( 'submit', function( e )
        {
            // preventing the duplicate submissions if the current one is in progress
            if( form.classList.contains( 'is-uploading' ) ) return false;

            form.classList.add( 'is-uploading' );
            form.classList.remove( 'is-error' );


                e.preventDefault();

                // gathering the form data
                var ajaxData = new FormData( form );
                console.log('file: ', file);
                console.log ('input name: ' , input.getAttribute( 'name' ));
                if( droppedHandle )
                {
                    console.log('df(0): ' , droppedFiles.item(0));
                    ajaxData.set('file', droppedFiles.item(0));
                }
                else
                {
                    ajaxData.append(input.getAttribute( 'name' ), file);
                }
                
                console.log('ajaxData: ', ajaxData);
            
                if (filename.localeCompare("") == 0)
                    {
                        error = true;
                        displayError("Please select a file to upload");
                        console.log("here");
                    }
                else if (filename.split('.').pop().localeCompare('txt') != 0)
                    {
                        error = true;
                        displayError("Please select .txt file");
                    }

                // ajax request
                var ajax = new XMLHttpRequest();
                ajax.responseType = 'json';
                ajax.open( form.getAttribute( 'method' ), url, true );
                console.log('url:' + url);

                ajax.onload = function()
                {
                    var res = ajax.response;
                    console.log(res);
                    form.classList.remove( 'is-uploading' );
                    if( !res.success ) errorMsg.textContent = res.error;
                    if( ajax.status >= 200 && ajax.status < 400 )
                    {
                        var data = res;
                        form.classList.add( data.success == true ? 'is-success' : 'is-error' );
                        if( !data.success  || error) 
                            {
                                errorMsg.textContent = data.error;
                                displayError(data.error);
                            }
                            
                    }
                    else console.log('Error. Please, contact the webmaster!');
                };

                ajax.onerror = function()
                {
                    form.classList.remove( 'is-uploading' );
                    console.log( 'Error. Please, try again!' );
                };

                ajax.send( ajaxData );
        });

        // restart the form if has a state of error/success
        Array.prototype.forEach.call( restart, function( entry )
        {
            errorAlert.style = "display: none";
            entry.addEventListener( 'click', function( e )
            {
                e.preventDefault();
                form.classList.remove( 'is-error', 'is-success' );
                input.click();
            });
        });

        // Firefox focus bug fix for file input
        input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
        input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });

    });
}( document, window, 0 ));