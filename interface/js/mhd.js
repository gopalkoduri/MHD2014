var current_elements = {images: [], sounds: []};
var make_embed_sound = function (sound) {
        "use strict";
        return "<div class=\"sound\" " + "id=\"" + sound.id + "\">" +
            "<img src=\"/interface/images/thumbsup-small.png\" class=\"click\" onclick=\"click_element('s'," + sound.id + ")\" />" +
            "<iframe class=\"content\" frameborder=\"0\" scrolling=\"no\" src=\"" +
            sound.embed_url + "\" width=\"481\" height=\"86\"></iframe></div>";
    };

var make_embed_image = function (image) {
        "use strict";
        return "<div class=\"image\" " + " id=\"" + image.id + "\">" +
            "<img src=\"/interface/images/thumbsup-small.png\" class=\"click\" onclick=\"click_element('p'," + image.id + ")\" />" +
            "<img class=\"content\" src=\"" + image.embed_url + "\" /></div>";
    };

var click_element = function(type, target) {
    $("#progressbar").progressbar("option", "value", 0);
    console.log("getting more things like  " +  target);
    var current_ids = {images: [], sounds: []};

    $.each(current_elements.images, function(index, image) {
        current_ids.images.push(image.id);
    });

    $.each(current_elements.sounds, function(index, sound) {
        current_ids.sounds.push(sound.id);
    });

    $.ajax({
        settings: {
            contentType: "application/json",
            },
            url:"http://localhost:5000/" + type + '/' + target,
        type: "POST",
        data: JSON.stringify(current_ids),
        success: build_gui,
        fail: function() { console.log("error getting moar sounds and images") }
    });
};

var build_gui = function(data) {
    console.log(data);
    current_elements = data;
    $("#photo_container").empty();
    $.each(data.images, function(index, element) {
        if (index < 10) {
            $("#photo_container").append(make_embed_image(element));
        }
    });
    $("#sound_container").empty();
    $.each(data.sounds, function(index, element) {
        if (index < 10) {
            $("#sound_container").append(make_embed_sound(element));
        }
    });
};
