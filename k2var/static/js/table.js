$(function() {
    $('#summary').DataTable({
        processing: false,
        pageLength: 25,
        ajax: {
            url: "https://spreadsheets.google.com/feeds/list/11Y0WIAQwOVJi-2mP9oVEzHg1EActd6sNxaYfwZT1SB4/od6/public/values?alt=json",
            dataSrc: "feed.entry",
        },
        columns: [
            { "data": "gsx$epicid.$t" },
            { "data": "gsx$type.$t" },
            { "data": "gsx$range.$t" },
            { "data": "gsx$period.$t" },
            { "data": "gsx$amplitude.$t" },
            { "data": "gsx$proposal.$t" },
        ],
    });
});
