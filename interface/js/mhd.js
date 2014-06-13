var current_elements = {images:[], sounds:[]}
make_embed_sound = function(sound) {
    return "<div class=\"sound\" " + "id=\"" + sound.id + "\">" +
        "<img src=\"/interface/images/thumbsup-small.png\" class=\"click\" onclick=\"click_element(" +sound.id + ")\"></div>" +
           "<iframe frameborder=\"0\" scrolling=\"no\" src=\"" +
           sound.embed_url + "\" width=\"481\" height=\"86\"></iframe></div>";
};

make_embed_image = function(image) {
    return "<div class=\"image\" " + " id=\"" +image.id + "\">" +
        "<img src=\"/interface/images/thumbsup-small.png\" class=\"click\" onclick=\"click_element(" + image.id + ")\"></div>" +
        "<img src=\"" + image.embed_url+ "\"></div>";
}

click_element = function(target) {
    console.log(target);
    var current_ids = {images: [], sounds: []}

    var type;
    $.each(current_elements.images, function(index, image) {
        current_ids.images.push(image.id);
        if (image.id === target) {
            type = 'p';
        }
    });

    $.each(current_elements.sounds, function(index, sound) {
        current_ids.sounds.push(sound.id);
        if (sound.id === target) {
            type = 's';
        }
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
}

build_gui = function(data) {
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

    
