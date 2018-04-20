'use strict';

var _utils = require('../utils.js');

var appTracking = new Vue({
    el: '#app-tracking',
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        currentItem: null
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        if (this.$el) {
            this.fetchData();
            this.pingTracking();
        }
    },

    methods: {
        checkJob: function checkJob(job) {
            _utils.utils.checkJob(job, this);
        },
        jobSuccess: function jobSuccess() {
            this.fetchData();
        },
        pingTracking: function pingTracking() {
            this.loading = true;
            _utils.utils.pingData('/api/pingtracking/', this);
        },
        fetchData: function fetchData() {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/trackevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    self.items = data;
                    if (data && data[0].tracks) {
                        data[0].tracks = data[0].tracks.slice().sort(function (a, b) {
                            return a.container.number.localeCompare(b.container.number);
                        });
                        self.currentItem = data[0].tracks[0];
                    }
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function open(url) {
            window.location.href = url;
        },
        clearSearch: function clearSearch() {
            this.search = "";
        },
        setCurrentItem: function setCurrentItem(item) {
            this.currentItem = item;
        },
        itemTracks: function itemTracks(item) {
            if (item) {
                var tracks = item.tracks;
                var self = this;
                return tracks.filter(function (track) {
                    if (!self.search) {
                        return true;
                    }
                    return track.container.number.search(new RegExp(self.search, "i")) != -1;
                });
            }
        }
    },
    filters: {
        shortdate: function shortdate(date) {
            return _utils.utils.shortdate(date);
        },
        moment: function moment(date) {
            return _utils.utils.moment(date);
        },
        upper: function upper(date) {
            return _utils.utils.upper(date);
        }
    }
});