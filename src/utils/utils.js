export const loadPiodide = async (stdRedir) => {
	console.log('loading prep');
	const pkgResponse = fetch('vpython.zip').then((x) => x.arrayBuffer());

	let pyodide = await loadPyodide({
		indexURL: 'https://cdn.jsdelivr.net/pyodide/dev/full/',
		stdout: stdRedir ? stdRedir : null,
		stderr: stdRedir ? stdRedir : null
	});

	const pkgdata = await pkgResponse;
	console.log('Unpacking package');
	pyodide.unpackArchive(pkgdata, 'zip');
	console.log('Importing vpython package');

	return pyodide;
};

export const setupGSCanvas = async () => {
	let display, scene;

	window.__context = {
		glowscript_container: $('#glowscript').removeAttr('id')
	};
	display = window.canvas;
	scene = display();
	return scene;
};
