'use strict';

var config = require( './grunt/config' );

module.exports = function ( grunt ) {

	require( 'jit-grunt' )( grunt );
	require( 'time-grunt' )( grunt );

	var configs = require( 'load-grunt-configs' )( grunt, config.options );
	grunt.initConfig( configs );

	grunt.registerTask( 'test', [
		'pylint'
	] );

	grunt.registerTask( 'default', [
		'test'
	] );

	grunt.registerTask( 'dist', [
		'test',
		'clean:dist',
		'copy:dist',
		'copy:gitignore_dist',
		'regex-replace:dist'
	] );

};