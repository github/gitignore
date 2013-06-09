<?php
/**
 * PHP script that can be used to generate a gitignore file listing all files currently defined
 * within a localhost repository. Useful for creating extensions for a core PHP package or
 * for Site Builders so that only add-on extensions and templates, etc., are saved to github.
 * 
 * To use:
 * 1. Copy to the root of your localhost PHP website
 * 2. Navigate to this file using your browser (ex. http://localhost/phpsite/CreatePhpGitignore.php
 * 3. Look for the gitignore.txt file on the root of the website.
 * 4. Rename to .gitignore
 *
 * If the file does not exist, make certain permissions are set correctly.
 */

$ignore = array();

$ignore[] = '.buildpath' . "\n";
$ignore[] = '.DS_Store' . "\n";
$ignore[] = '.idea' . "\n";
$ignore[] = '.project' . "\n";
$ignore[] = '.settings' . "\n";
$ignore[] = '.gitignore' . "\n";
$ignore[] = '.gitattributes' . "\n";
$ignore[] = 'composer.phar' . "\n";
$ignore[] = 'composer.lock' . "\n";

$current_path = __DIR__;

$objects = new RecursiveIteratorIterator
(new RecursiveDirectoryIterator($current_path),
    RecursiveIteratorIterator::SELF_FIRST);

$dirRead = dir(__DIR__);
$path    = $dirRead->path;
while ($entry = $dirRead->read()) {
    if ($entry == '.' || $entry == '..' || $entry == '.git') {

    } else {
        if (is_dir($path . '/' . $entry)) {
        } else {
            $item     = $path . '/' . $entry;
            $ignore[] = substr($item, strlen($current_path) + 1, 99999) . "\n";
        }
    }
}
$dirRead->close();

foreach ($objects as $name => $object) {

    if ($object->isDir()) {
        if (basename($name) == '.' || basename($name) == '..' || basename($name) == '.git') {
        } else {
            $test = substr(substr($name, strlen($current_path) + 1, 9999), 0, 4);
            if ($test == '.git') {
            } else {
                $dirRead = dir($name);
                $path    = $dirRead->path;
                while ($entry = $dirRead->read()) {
                    if (is_dir($path . '/' . $entry)) {
                    } else {
                        $item     = $path . '/' . $entry;
                        $ignore[] = substr($item, strlen($current_path) + 1, 99999) . "\n";
                    }
                }
                $dirRead->close();
            }
        }
    }
}

file_put_contents('gitignore.txt', $ignore);

