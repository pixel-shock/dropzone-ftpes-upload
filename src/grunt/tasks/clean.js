module.exports = function ( grunt, options ) {

	var packageInfo = grunt.file.readJSON('./package.json');
	var distName = 'v' + packageInfo.version;
	var cleanPath = grunt.template.process('<%= paths.dist %>/' + distName, {
		data: {
			paths: options.paths,
			distName: distName
		}
	});

	return {
		dist: {
			options: {
				force: true
			},
			src: [ cleanPath ]
		}
	};
};