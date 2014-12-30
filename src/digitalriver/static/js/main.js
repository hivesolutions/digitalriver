(function(jQuery) {
    jQuery.fn.ulog = function(options) {
        // retrieves the reference to the currently matched
        // object that is going to be used as the curren context
        var matchedObject = this;

        var initialize = function(element) {
            var url = element.attr("data-url");
            var key = element.attr("data-key");
            var channel = element.attr("data-channel");
            var pushi = new Pushi(key, {
                        baseUrl : url
                    });

            pushi.bind("connect", function(event) {
                        pushi.subscribe(channel);
                    });

            pushi.bind("stdout", function(event, data, channel) {
                        data = data.replace("\n", "<br/>");
                        data = data.replace(" ", "&nbsp;");
                        element.append("<div class=\"line\">" + data + "</div>");
                        scrollBottom(element);
                    });

            // if the current pushi connection for the url is already connected
            // then the subscription process is executed immediately
            var isConnected = pushi.state == "connected";
            isConnected && pushi.subscribe(channel);

            // schedules a next tick operation to scroll the current element down
            // so that the proper initial log contents are display properly
            setTimeout(function() {
                        scrollBottom(element);
                    });
        };

        var scrollBottom = function(element) {
            var scrollHeight = element[0].scrollHeight;
            element.scrollTop(scrollHeight);
        };

        // iterates over the complete set of element in the
        // matched object to be able to initialize the elements
        matchedObject.each(function(element, index) {
                    var _element = jQuery(this);
                    initialize(_element);
                });

        // returns the object to the caller function/method
        // so that it may be chained in other executions
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.uprovision = function(options) {
        // retrieves the reference to the currently matched
        // object that is going to be used as the curren context
        var matchedObject = this;

        // retrieves the associated (hidden) field that contains
        // the droplet id and then gathers its value
        var dropletIdField = jQuery("[name=droplet_id]", matchedObject);
        var dropletId = dropletIdField.uxvalue();

        // retrieves the reference to the url field so that it's
        // possible to register for any change in such element that
        // will trigger a remote request to the server side
        var urlField = jQuery("[name=url]", matchedObject);
        urlField.bind("value_change", function() {
            // retrieves the current element refernece and uses it
            // to gather the parent provision container
            var element = jQuery(this);
            var provision = element.parents(".provision");

            // gathers the reference to the extras element of the
            // provision and empties it of any element (new config)
            var extras = jQuery(".extras", provision);
            extras.empty();

            // retrieves the (url) value of the current element, this is
            // going to be used as the basis in the remote request
            var value = element.uxvalue();

            // runs the remote call for the processing of the requested
            // torus configuration file (using http), this should return
            // a proper json encoded config file from which the configuration
            // lines may be extracted and used for configuration
            jQuery.ajax({
                url : "/droplets/" + dropletId + "/process",
                data : {
                    url : value
                },
                error : function(request, status, error) {
                },
                success : function(data) {
                    var config = data.config;
                    if (!config) {
                        return;
                    }

                    for (var index = 0; index < config.length; index++) {
                        var item = config[index];
                        extras.append("<input type=\"hidden\" name=\"names\" value=\""
                                + item.name + "\" />");
                        extras.append("<div class=\"label\">" + "<label>"
                                + item.name + "</label>" + "</div>");
                        extras.append("<div class=\"input\">"
                                + "<input class=\"text-field\" name=\"values\" value=\""
                                + item["default"] + "\" />" + "</div>");
                    }
                }
            });
        });

        // returns the object to the caller function/method
        // so that it may be chained in other executions
        return this;
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the reference to the currently matched log
        // objects and starts the log extension in all of them
        var log = jQuery(".log", matchedObject);
        log.ulog();

        // retrieves the reference to the provision element and
        // then registers the proper extension in it
        var provision = jQuery(".provision", matchedObject);
        provision.uprovision();
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
