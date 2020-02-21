'use strict';

;( function ( document, window, index )
{
    var docUrl = document.location.href;
    var userId = docUrl.split('?').pop();
    var url = "https://groop.pw:3000/files/upload?" + userId;
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
                hideError();
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
            hideError();
            // preventing the duplicate submissions if the current one is in progress
            if( form.classList.contains( 'is-uploading' ) ) return false;

            form.classList.add( 'is-uploading' );
            form.classList.remove( 'is-error' );


                e.preventDefault();

                // gathering the form data
                var ajaxData = new FormData( form );
                if( droppedHandle )
                {
                    ajaxData.set('file', droppedFiles.item(0));
                }
                else
                {
                    ajaxData.append(input.getAttribute( 'name' ), file);
                }
            
                if (filename.localeCompare("") == 0)
                    {
                        error = true;
                        displayError("Please select a file to upload");
                    }
                else if (filename.split('.').pop().localeCompare('txt') != 0)
                    {
                        error = true;
                        displayError("Please select .txt file");
                    }

                // ajax request
                var ajax = new XMLHttpRequest();
                ajax.open('POST', url, true );
                ajax.responseType = 'json';
                ajax.withCredentials = false;
                console.log('url:' + url);

                ajax.onload = function()
                {
                    form.classList.remove( 'is-uploading' );
                    
                    var res = ajax.response;
                    console.log(res);
                    if( !res.success ) errorMsg.textContent = res.error;
                    
                    if (res.success)
                        {
                            hideError();
                            form.classList.add('is-success');
                            console.log('success through res');
                            window.location.replace("https://groop.pw/dashboard.html?" + id);
                        }
                    else if( ajax.status >= 200 && ajax.status < 400 )
                    {
                        var data = res;
                        form.classList.add( data.success == true ? 'is-success' : 'is-error' );
                        if( !data.success  || error) 
                            {
                                errorMsg.textContent = data.error;
                                displayError(data.error);
                            }
                        else
                            {
                                hideError();
                            }
                            
                    }
                    else if (ajax.status == 500)
                        {
                            errorMsg.textContent = res.error;
                            displayError("Server error, try again later.");
                        }
                    else
                        {
                            errorMsg.textContent = res.error;
                            displayError(res.error);
                        }
                };

                ajax.onerror = function()
                {
                    form.classList.remove( 'is-uploading' );
                    console.log( 'Error. Please, try again!' );
                    displayError('Error. Please, try again');
                };

                ajax.onabort = function()
                {
                    displayError('Error. Please check your internet conenction and try again');
                }
                hideError();
                ajax.send( ajaxData );
                
        });

        // restart the form if has a state of error/success
        Array.prototype.forEach.call( restart, function( entry )
        {
            hideError();
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