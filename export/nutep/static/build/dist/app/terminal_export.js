'use strict';

var _utils = require('../utils.js');

Vue.component('v-select', VueSelect.VueSelect);

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    components: {
        vuejsDatepicker: vuejsDatepicker
    },
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        currentItem: null,
        container: null,
        stats: {
            total_rows: 0
        },
        filter: {
            number: '',
            size: [],
            type: [],
            line: [],
            date: null,
            contract: [],
            terminal: []
        },
        highlighted: {
            dates: [new Date()]
        }
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        this.fetchData();
        this.pingData();
    },

    computed: {
        isFiltered: function isFiltered() {
            return this.filter.number || this.filter.size.length || this.filter.type.length || this.filter.line.length || this.filter.date || this.filter.contract.length || this.filter.terminal.length;
        },
        filterOptions: function filterOptions() {
            var result = {
                sizes: [],
                lines: [],
                types: [],
                contracts: [],
                terminals: []
            };
            if (this.items.length == 0) {
                return result;
            }

            var rows = this.items[0].terminalexports;
            var sizes = new Set();
            var types = new Set();
            var lines = new Set();
            var contracts = new Set();
            var terminals = new Set();
            rows.forEach(function (elem, i, arr) {
                if (elem.container) {
                    sizes.add(elem.container.size);
                    lines.add(elem.container.line);
                    types.add(elem.container.type);
                    if (elem.container.contract) {
                        contracts.add(elem.container.contract);
                    }
                    terminals.add(elem.container.terminal);
                }
            });
            result.sizes = Array.from(sizes);
            result.lines = Array.from(lines);
            result.types = Array.from(types);
            result.contracts = Array.from(contracts);
            result.terminals = Array.from(terminals);
            return result;
        }
    },
    methods: {
        customFormatter: function customFormatter(date) {
            return moment(date).format('DD.MM.YYYY');
        },

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
            this.filter.number = "";
        },
        clearDate: function clearDate() {
            this.filter.date = null;
            console.log('OK');
        },
        clearFilter: function clearFilter() {
            this.filter.number = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.line = [];
            this.filter.contract = [];
            this.filter.terminal = [];
            this.filter.date = null;
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
                var filtered = rows.filter(function (row) {
                    if (!self.isFiltered) {
                        return true;
                    }
                    if (self.filter.number && !(row.container.number.search(new RegExp(self.filter.number, "i")) != -1)) {
                        return false;
                    }
                    if (self.filter.type.length && !self.filter.type.includes(row.container.type)) {
                        return false;
                    }
                    if (self.filter.size.length && !self.filter.size.includes(row.container.size)) {
                        return false;
                    }
                    if (self.filter.line.length && !self.filter.line.includes(row.container.line)) {
                        return false;
                    }
                    if (self.filter.contract.length && !self.filter.contract.includes(row.container.contract)) {
                        return false;
                    }
                    if (self.filter.terminal.length && !self.filter.terminal.includes(row.container.terminal)) {
                        return false;
                    }
                    if (self.filter.date && !(moment(self.filter.date).format('YYYY-MM-DD') == row.container.datein)) {
                        return false;
                    }
                    return true;
                });
                self.stats.total_rows = filtered.length;
                self.stats.total_unfiltered = rows.length;
                return filtered;
            }
        }
    },
    filters: {
        shortdate: function shortdate(date) {
            return _utils.utils.shortdate(date);
        },
        date: function date(_date) {
            return _utils.utils.date(_date);
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