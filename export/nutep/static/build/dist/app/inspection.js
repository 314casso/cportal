'use strict';

function getHhmm(value) {
	if (value == 0) return moment.utc(0).format('HH:mm');
	var duration = moment.duration(value * 1000);
	return duration.format("hh:mm", { trim: false });
}

var app = new Vue({
	el: '#inspection',
	delimiters: ["<%", "%>"],
	data: {
		curdoc: null,
		info: null,
		errors: [],
		loading: false,
		error: '',
		data: [],
		index: null,
		inspection: {}
	},
	created: function created() {
		this.loadData();
	},
	computed: {
		sortedDate: function sortedDate() {
			return this.data.sort(function (a, b) {
				return new Date(b.date) - new Date(a.date);
			});
		},
		inspectionImages: function inspectionImages() {
			if (this.inspection.files) {
				return this.inspection.files.filter(function (image) {
					return image.extension != 'pdf';
				});
			}
			return [];
		},
		inspectionDocs: function inspectionDocs() {
			if (this.inspection.files) {
				return this.inspection.files.filter(function (image) {
					return image.extension == 'pdf';
				});
			}
			return [];
		}
	},
	methods: {
		loadData: function loadData() {
			var _this = this;

			this.errors = [];
			this.loading = true;
			fetch('/inspections/').then(function (res) {
				_this.updated = new Date();
				_this.status = res.status;
				if (res.status !== 200) {
					err = {};
					err.message = getShortDate(_this.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
					_this.errors.push(err);
					_this.loading = false;
					return;
				};

				res.json().then(function (json) {
					_this.data = JSON.parse(json);
					_this.loading = false;
				});
			});
		},
		loadItem: function loadItem(guid) {
			var _this2 = this;

			this.errors = [];
			this.loading = true;
			fetch('/api/inspection/' + guid + '/?format=json').then(function (res) {
				if (res.status !== 200) {
					err = {};
					err.message = getShortDate(_this2.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
					_this2.errors.push(err);
					_this2.loading = false;
					return;
				};

				res.json().then(function (json) {
					_this2.inspection = json;
					_this2.loading = false;
				});
			});
		},
		resetItem: function resetItem(guid) {
			var _this3 = this;

			this.errors = [];
			this.loading = true;
			fetch('/getinspection/' + guid + '/').then(function (res) {
				if (res.status !== 200) {
					err = {};
					err.message = getShortDate(_this3.updated) + '. Ошибка загрузки данных. Ответ сервера: ' + res.status;
					_this3.errors.push(err);
					_this3.loading = false;
					return;
				};

				res.json().then(function (json) {
					_this3.loadItem(guid);
					_this3.loading = false;
				});
			});
		},
		containerClick: function containerClick(curdoc) {
			this.curdoc = curdoc;
			this.loadItem(curdoc.guid);
			// $('.collapse').collapse('toggle');            
		}
	},
	filters: {
		hhmm: function hhmm(value) {
			return getHhmm(value);
		},
		shortdate: function shortdate(date) {
			return getShortDate(date);
		},
		humanFileSize: function humanFileSize(bytes) {
			return _humanFileSize(bytes, true);
		}
	}
});

function getShortDate(date) {
	if (date) {
		return moment(date).format('DD.MM.YYYY');
	}
}

function _humanFileSize(bytes, si) {
	var thresh = si ? 1000 : 1024;
	if (Math.abs(bytes) < thresh) {
		return bytes + ' B';
	}
	var units = si ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'] : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
	var u = -1;
	do {
		bytes /= thresh;
		++u;
	} while (Math.abs(bytes) >= thresh && u < units.length - 1);
	return bytes.toFixed(1) + ' ' + units[u];
}

$(document).on('click', '[data-toggle="lightbox"]', function (event) {
	event.preventDefault();
	$(this).ekkoLightbox();
});