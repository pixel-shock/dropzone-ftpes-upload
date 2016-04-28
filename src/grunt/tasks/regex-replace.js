module.exports = function ( grunt, options ) {

	var uuid = require( 'node-uuid' );
	var packageInfo = grunt.file.readJSON( './package.json' );
	var distName = 'v' + packageInfo.version;
	var actionFile = grunt.template.process( '<%= paths.dist %>/' + distName + '/' + packageInfo.dropzone_name + '/action.py', {
		data: {
			paths: options.paths,
			distName: distName
		}
	} );

	return {
		dist: {
			src: [ actionFile ],
			actions: [
				{
					name: 'uniqueId',
					search: new RegExp( /(#\s?UniqueID:\s)(.*)/gi ),
					replace: function ( matched_string, substring_match1 ) {
						console.log( matched_string, substring_match1 );
						return substring_match1 + uuid.v4();
					}
				},
				{
					name: 'version',
					search: new RegExp( /(#\s?Version:\s)(.*)/gi ),
					replace: function ( matched_string, substring_match1 ) {
						console.log( matched_string, substring_match1 );
						return substring_match1 + packageInfo.version;
					}
				}
			]
		}
	};
};