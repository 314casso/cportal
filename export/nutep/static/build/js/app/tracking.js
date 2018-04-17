import {utils} from '../utils.js';

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
    mounted() {
        if (this.$el) {
            this.fetchData();
            this.pingTracking();
        }
    },
    methods: {
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccess: function () {
            this.fetchData();
        },
        pingTracking: function () {
            this.loading = true;
            utils.pingData('/api/pingtracking/', this);
        },
        fetchData: function () {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/trackevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
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
        open: function (url) {
            window.location.href = url;
        },
        clearSearch: function () {
            this.search = "";
        },
        setCurrentItem: function (item) {
            this.currentItem = item;
        },
        itemTracks: function (item) {
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
        },
    },
    filters: {
        shortdate: function (date) {
            return utils.shortdate(date);
        },
        moment: function (date) {				
            return utils.moment(date);									
        },
        upper: function (date) {
            return utils.upper(date);					
        },
    },
});