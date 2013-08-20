;
(function () {
    var app = {
        init: function () {
            this.facebook.setup();
            this.form.setup();
        },
        form: {
            setup: function () {
                this.emailChange();

                $('.apollo-register-account .register-link').click(function (e) {
                    e.preventDefault();

                    $('.apollo-login').fadeOut(350, function(){
                    	$('.apollo-register').fadeIn(350, function(){
                    		$('.apollo-register input:first').focus();
                    	});
                    	$('.apollo').addClass('register');
                    });
                });

                $('.apollo-back a').click(function (e) {
                    e.preventDefault();

                     $('.apollo-register:visible, .apollo-forgotten-password:visible').fadeOut(350, function(){
                    	$('.apollo-login').fadeIn(350);
                    	// $('.apollo').removeClass('register forgotten-password');
                    });
                });

                $('.apollo-register-account .password-link').click(function (e) {
                    e.preventDefault();

                    $('.apollo-login').fadeOut(350, function(){
                    	$('.apollo-forgotten-password').fadeIn(350, function(){
                    		$('.apollo-forgotten-password input:first').focus();
                    	});
                    	$('.apollo').addClass('forgotten-password');
                    });
                });

                $('#apollo-register-form').submit(function(e){
                	e.preventDefault();

                	app.form.handleRegister($(this));
                });

                 $('#apollo-forgotten-password-form').submit(function(e){
                	e.preventDefault();

                	app.form.handleForgottenPassword($(this));
                });

                $('#apollo-login-form').submit(function(e){
                	e.preventDefault();

                	app.form.handleStandardLogin($(this));
                });
            },
            emailChange: function () {
                $('.email').change(function () {
                    var t = $(this),
                        md5 = MD5($.trim(t.val().toLowerCase())),
                        gravatar = 'http://www.gravatar.com/avatar/' + md5 + '?d=http://tidy.eideus.com/img/avatar.png&s=205';

                   	$('.apollo-image').css('backgroundImage', 'none');
                    $('<img />').attr('src', gravatar).imagesLoaded(function(){
                		$('.apollo-image').css('backgroundImage', 'url(' + gravatar + ')');
                    });
                    
                });
            },
            handleStandardLogin: function (form) {
            	if(app.checkUserAccount('standard', form)){ // The user has an account and the details are valid...
            		$('.apollo-login').fadeOut(350, function(){
						$('.apollo-logging-in').fadeIn(350);
					});
            	}
            	else { // The details were invalid...
            		var login = $('.apollo-login'),
            			email = login.find('[type="text"]').parents('.control-group'),
            			password = login.find('[type="password"]').parents('.control-group');

            		password.addClass('error');
            		email.addClass('error').find('input').popover({
            			title: 'Ooops!',
            			content: 'Your email address / password appear to be incorrect. Please verify them and try logging in again.',
            			trigger: 'manual',
            			placement: 'right'
            		}).popover('show');
        		}	           	
            },
            handleRegister: function (form) {
            	var fName = $('#firstName').val(),
            		data = form.serialize();

            	if(app.checkUserAccount('register', form)){
					var register = $('.apollo-register'),
            			email = register.find('[type="text"]:first').parents('.control-group');

            		email.addClass('error').find('input:first').popover({
            			title: 'Ooops!',
            			content: 'It looks like you already have an account with that email address.',
            			trigger: 'manual',
            			placement: 'right'
            		}).popover('show');
            	}
            	else {
            		if(fName.length){
	            		$('.user-name').text(', '+fName);
	            	}

					$('.apollo-register').fadeOut(350, function(){
						$('.apollo-registering').fadeIn(350);
					});
            	}

				// Handle the user's details (data) here via AJAX...
            },
            handleForgottenPassword: function(form){
            	if(app.checkUserAccount('forgottenPassword', form)){
            		$('.apollo-forgotten-password').fadeOut(350, function(){
						$('.apollo-password-reset').fadeIn(350);
					});
            	}
            	else {
					var fPassword = $('.apollo-forgotten-password'),
            			email = fPassword.find('[type="text"]:first').parents('.control-group');

            		email.addClass('error').find('input:first').popover({
            			title: 'Ooops!',
            			content: 'It looks like we don\'t have an account registered with that email address.',
            			trigger: 'manual',
            			placement: 'right'
            		}).popover('show');
            	}

				// Handle the user's details (data) here via AJAX...
            }
        },
     	checkUserAccount: function(loginType, data){
     		// This is where you'd check the account details via Ajax...
     		return ($('[name="optionsRadios"]:checked').val() == 'yes');
        },
        facebook: {
            setup: function () {
                /* Enter your own Facebook App details here... */
                window.fbAsyncInit = function () {
                    FB.init({
                            appId: '465771293512015',
                            channelUrl: '//tidy.eideus.com/js/lib/channel.js',
                            status: true,
                            xfbml: true
                        });

                    app.facebook.init();
                };

                /* This loads the FB SDK asyncronously... */
                (function (d, s, id) {
                        var js, fjs = d.getElementsByTagName(s)[0];
                        if(d.getElementById(id)) {
                            return;
                        }
                        js = d.createElement(s);
                        js.id = id;
                        js.src = "//connect.facebook.net/en_US/all.js";
                        fjs.parentNode.insertBefore(js, fjs);
                    }(document, 'script', 'facebook-jssdk'));
            },
            init: function () {
                $('.btn-facebook').on('click', function (e) { // When the Facebook button is clicked...
                        e.preventDefault();

                        FB.login(function(response){
		                	app.facebook.loginSuccess(response);
		                }, {
                            scope: "email"
                        });
                    });

                FB.getLoginStatus(function(response){
                	app.facebook.loginSuccess(response);
                }, {
                    scope: "email"
                });
            },
            loginSuccess: function(response){
            	if(response.status === 'connected') {
                    var uid = response.authResponse.userID,
                        accessToken = response.authResponse.accessToken;

                    FB.api('/me', function (response) { // Get the user's details
                    	$('.apollo-image').css('backgroundImage', 'none');
                    	
                    	var src = 'http://graph.facebook.com/'+response.username+'/picture?width=205&height=205',
                    		img = $('<img />').attr('src', src).imagesLoaded(function(){
                    			$('.apollo-image').css('backgroundImage', 'url(' + src + ')');
                    		});

                    	if(app.checkUserAccount('facebook', response)){
                    		$('.user-name').text(', '+response.first_name);
							$('.apollo-login').fadeOut(350, function(){
								$('.apollo-logging-in').fadeIn(350);
							});
                    	}
                    	else {
                    		$('#firstName').val(response.first_name);
                    		$('#lastName').val(response.last_name);
                    		$('#registerEmail').val(response.email);
                    		$('.apollo-login').fadeOut(350, function(){
								$('.apollo-register').fadeIn(350, function(){
									$('#apollo-register-form [type="password"]:first').focus();
								});
							});
                    	}
                    });
                }
            }
        },
        domReady: function () {},
        windowLoad: function () {}
    };

    app.init();
    $(function () {
            app.domReady();

            $(window).load(app.windowLoad);
        });

})(jQuery)