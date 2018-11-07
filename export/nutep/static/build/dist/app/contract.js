'use strict';

var _utils = require('../utils.js');

Vue.component('v-select', VueSelect.VueSelect);

var appTerminalExport = new Vue({
    el: '#app-terminal-export',
    data: {
        items: [],
        loading: false,
        error: '',
        search: '',
        stats: {
            total_rows: 0
        },
        filter: {
            name: '',
            size: [],
            type: [],
            extension: []
        },
        contracts: [],
        contract: null
    },
    delimiters: ["<%", "%>"],
    mounted: function mounted() {
        this.fetchContracts();
        this.pingContracts();
    },

    computed: {
        isFiltered: function isFiltered() {
            return this.filter.name || this.filter.type.length || this.filter.extension.length;
        },
        filterOptions: function filterOptions() {
            var result = {
                extensions: [],
                types: []
            };
            if (this.items.length == 0) {
                return result;
            }

            var rows = this.items[0].contractevent.files;

            if (!rows) {
                return result;
            }
            var types = new Set();
            var extensions = new Set();

            rows.forEach(function (elem, i, arr) {
                if (elem) {
                    extensions.add(elem.extension);
                    types.add(elem.doc_type);
                }
            });
            result.extensions = Array.from(extensions);
            result.types = Array.from(types);
            result.types.sort();
            return result;
        }
    },
    watch: {
        contract: function contract(val) {
            if (val) {
                this.pingContractFiles(val);
            } else {
                this.fetchContractFiles();
            }
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
            this.fetchContracts();
            this.fetchContractFiles();
            console.log(this.filterOptions);
        },
        pingContracts: function pingContracts() {
            this.loading = true;
            _utils.utils.pingData('/pingcontracts/', this);
        },
        pingContractFiles: function pingContractFiles(contract) {
            this.loading = true;
            _utils.utils.pingData('/pingcontractfiles/' + contract.id + '/', this);
        },
        fetchContractFiles: function fetchContractFiles() {
            var _this = this;

            if (!this.contract) {
                this.items = [];
                this.stats.total_rows = 0;
                this.stats.total_unfiltered = 0;
                return;
            }
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/contractfiles/?contract=' + this.contract.id);
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    _this.items = data;
                } catch (e) {
                    _this.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        fetchContracts: function fetchContracts() {
            var _this2 = this;

            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/api/contracts/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText, _utils.utils.reviver);
                    _this2.contracts = data;
                } catch (e) {
                    _this2.error = "Произошла ошибка обновления данных: " + e;
                }
            };
            xhr.send();
        },
        open: function open(file) {
            var wnd = window.open('about:blank', '_blank');
            var xhr = new XMLHttpRequest();
            var self = this;
            xhr.open('GET', '/getfileurl/' + file.guid + '/');
            xhr.onload = function () {
                try {
                    var data = JSON.parse(xhr.responseText);
                    if (data.url) {
                        wnd.location = data.url;
                    }
                } catch (e) {
                    appSettings.error = "Произошла ошибка обновления данных: " + e + ": " + xhr.responseText;
                }
            };
            xhr.send();
        },
        clearSearch: function clearSearch() {
            this.filter.name = "";
        },
        clearDate: function clearDate() {
            this.filter.date = null;
            console.log('OK');
        },
        clearFilter: function clearFilter() {
            this.filter.name = '';
            this.filter.size = [];
            this.filter.type = [];
            this.filter.extention = [];
        },
        setContainer: function setContainer(terminalexport) {
            if (!terminalexport.container) {
                return false;
            }
            this.container = terminalexport.container;
            return true;
        },
        rows: function rows(item) {
            if (item && item.contractevent && item.contractevent.files) {
                var rows = item.contractevent.files.slice();

                rows.sort(function (a, b) {
                    if (a.doc_type > b.doc_type) {
                        return 1;
                    }
                    if (a.doc_type < b.doc_type) {
                        return -1;
                    }
                    return 0;
                });

                var self = this;
                var filtered = rows.filter(function (row) {
                    if (!self.isFiltered) {
                        return true;
                    }
                    if (self.filter.name && !(row.title.search(new RegExp(self.filter.name, "i")) != -1)) {
                        return false;
                    }
                    if (self.filter.type.length && !self.filter.type.includes(row.doc_type)) {
                        return false;
                    }
                    if (self.filter.extension.length && !self.filter.extension.includes(row.extension)) {
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
        },
        humanFileSize: function humanFileSize(size) {
            return _utils.utils.humanFileSize(size);
        }
    }
});