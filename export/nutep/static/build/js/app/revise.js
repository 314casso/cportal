import {utils} from '../utils.js';

var appRevise = new Vue({
    el: '#app-revise',
    data: {
        items: [],
        loading: false,
        error: ''
    },
    delimiters: ["<%", "%>"],
    mounted() {			
        if (this.$el) {
            this.fetchData();
            this.pingRevise();
        }
    },
    methods: {
        checkJob: function (job) {
            utils.checkJob(job, this);
        },
        jobSuccess: function () {
            this.fetchData();
        },
        pingRevise: function () {
            this.loading = true;
            utils.pingData('/api/pingrevise/', this);
        },
        fetchData: function () {
            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/api/reviseevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, utils.reviver);
                    self.items = data;						
                } catch (e) {
                    self.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function (url) {
            window.location.href = url;
        }
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