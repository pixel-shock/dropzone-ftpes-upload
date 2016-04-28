module.exports = function ( grunt, options ) {

	var packageInfo = grunt.file.readJSON('./package.json');
	var distName = 'v' + packageInfo.version;
	var outputPath = grunt.template.process('<%= paths.dist %>/' + distName + '/' + packageInfo.dropzone_name + '/', {
		data: {
			paths: options.paths,
			distName: distName
		}
	});
	var sourcePath = grunt.template.process('<%= paths.source %>/**/*.*', {
		data: {
			paths: options.paths
		}
	});

	return {
		dist: {
			files: [
				{
					expand: true,
					cwd: options.paths.source,
					src: [ '**/*.*' ],
					dest: outputPath
				}
			]
		},
		gitignore_dist: {
			files: [
				{
					expand: true,
					cwd: '../',
					src: [ '.gitignore' ],
					dest: outputPath
				}
			]
		}
	};
};