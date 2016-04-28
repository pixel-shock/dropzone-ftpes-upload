module.exports = function ( grunt, options ) {
	return {
		options: {
			rcfile: '.pylintrc'
		},
		dist: {
			src: 'dropzone'
		}
	};
};