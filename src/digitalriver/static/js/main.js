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

            pushi.subscribe(channel);
            pushi.bind("notification", function(event, data, channel) {
                        console.info(data);
                    });
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
        var log = matchedObject.filter(".log");
        log.ulog();
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
