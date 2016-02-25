# Add a decoration to the top of each gitignore file
require "find"

desc "Add decoration"
task :decorate do
  Dir.glob("**/*.gitignore") do |file| # note one extra "*"
    if FileTest.file?(file)
      if File.basename(file)[0] == ?.
        next
      else
        original_file = file
        new_file = file + '.new'
        File.open(new_file, 'w') do |fo|
          fo.puts "# ===== #{original_file} ===== #"
          File.foreach(original_file) do |li|
            fo.puts li
          end
        end
        # Finish up the job
        File.rename(original_file, original_file + '.old')
        File.rename(new_file, original_file)
      end
    end
  end
end

desc "Append newlines if not already present"
task :append do
  Dir.glob("**/*.gitignore") do |file| # note one extra "*"
    if FileTest.file?(file)
      if File.basename(file)[0] == ?.
        next
      else
        original_file = file
        new_file = file + '.new'
        File.open(new_file, 'w') do |fo|
          File.foreach(original_file) do |li|
            fo.puts li
          end
          fo.puts "\n"
        end
        # Finish up the job
        File.rename(original_file, original_file + '.old')
        File.rename(new_file, original_file)
      end
    end
  end
end

