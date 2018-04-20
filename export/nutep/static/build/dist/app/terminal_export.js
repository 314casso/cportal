'use strict';

var _utils = require('../utils.js');

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        currentItem: null,
        container: null
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        this.fetchData();
        this.pingData();
    },

    methods: {
        checkJob: function checkJob(job) {
            _utils.utils.checkJob(job, this);
        },
        jobSuccess: function jobSuccess() {
            this.fetchData();
        },
        pingData: function pingData() {
            this.loading = true;
            _utils.utils.pingData('/api/pingterminalexport/', this);
        },
        fetchData: function fetchData() {
            var _this = this;

            console.log("fetchData");
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/terminalexportevents/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    _this.items = data;
                    if (data && data[0].terminalexports) {
                        _this.currentItem = data[0].terminalexports[0];
                    }
                } catch (e) {
                    _this.error = "Произошла ошибка обновления данных: " + e;
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
        setContainer: function setContainer(terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;
            if (this.container.stuffs) {
                this.container.total = {
                    'netweight': _utils.utils.sum(this.container.stuffs, 'netweight'),
                    'grossweight': _utils.utils.sum(this.container.stuffs, 'grossweight'),
                    'quantity': _utils.utils.sum(this.container.stuffs, 'quantity')
                };
            }
            return true;
        },
        rows: function rows(item) {
            if (item) {
                var rows = item.terminalexports;
                var self = this;
                return rows.filter(function (row) {
                    if (!self.search) {
                        return true;
                    }
                    return row.container.number.search(new RegExp(self.search, "i")) != -1;
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
        },
        number: function number(x) {
            return _utils.utils.number(x);
        }
    }
});