(function() {
    function createElement(tag, parent, className, id) {
        var el = document.createElement(tag);
        el.className = className;
        if (id)
            el.id = id;
        parent.appendChild(el);
        return el;
    }

    function createTextElement(parent, className, text) {
        var el = document.createElement("span");
        el.className = className;
        el.innerHTML = text;
        parent.appendChild(el);
        return el;
    }

    function createWrapper(className) {
        var wrapper = createElement("div", document.body, className);
        var i1 = createElement("div", wrapper, "i1");
        createTextElement(i1, "text", "Item1");
        var i2 = createElement("div", wrapper, "i2");
        createTextElement(i2, "text", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.");
        var i3 = createElement("div", wrapper, "i3");
        createTextElement(i3, "text", "Item 3 longer");
    }

    function createTestFunction(limit, className) {
        return function() {
            for (var i = 0; i < limit; ++i)
                createWrapper(className);
        }
    }

    window.createFlexVSGridTestFunction = createTestFunction;
})();
