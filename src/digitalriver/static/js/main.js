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
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the reference to the currently matched log
        // objects and starts the log extension in all of them
        var log = jQuery(".log", matchedObject);
        log.ulog();
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
