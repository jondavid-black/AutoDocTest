require 'kramdown'
require 'pdfkit'

def process_doc_file(filepath)
    category = ""
    title = ""
    order = ""
    level = 0
    output = ""

    inMetadata = false
    File.open(filepath, "r") do |f|
        f.each_line do |line|
            if line.strip == "---"
                #puts "Found --- indicating metadata"
                if inMetadata
                    output += ('#' * level) + " " + order + " " + title + "\n"
                end
                inMetadata = !inMetadata
                next
            end 
            if inMetadata
                #puts "Processing line within metadata: #{line}"
                parts = line.split(":")
                if (parts[0].strip == "category")
                    category = parts[1].strip
                    next
                end
                if (parts[0].strip == "title")
                    title = parts[1].strip
                    next
                end
                if (parts[0].strip == "order")
                    order = parts[1].strip
                    order = order.gsub("'", "")
                    level = order.split(".").length()
                    next
                end
            end
            if !inMetadata
                #puts "Processing non-metadata line"
                if (line.start_with?("#"))
                    # make sure heading level is correct-ish
                    output += ('#' * level) + " " + line + "\n"
                else
                    # append line to output
                    output += line
                end
            end
        end
        output += "\n"
    end

    #puts "finished processing file: #{filepath}"
    #puts "category: #{category}   title: #{title}   order: #{order}   level: #{level}"
    return category, output
end

# Process a document directory
def process_dir(dirpath)
    docTitle = ""
    docContent = ""

    filenames = Dir.entries(dirpath)
    for filename in filenames.sort do
        next if filename == '.' or filename == '..' or filename == dirpath
        # Do work on the remaining files & directories
        output = process_doc_file("#{dirpath}/#{filename}")
        docTitle = output[0]
        docContent += output[1]
    end

    return docTitle, docContent
end

def updateTitle(src, dest, markings, title)

    text = File.read(src)
    new_contents = text.gsub("[[Document Markings]]", markings)
    new_contents = new_contents.gsub("[[Document Title]]", title)

    File.open(dest, "w") {|file| file.puts new_contents }

end
 
  
  if __FILE__ == $0
    

    filenames = Dir.entries("./_docs")
    for filename in filenames.sort do
        next if filename == '.' or filename == '..' or File.file?(File.join("./_docs", filename))
        # Do work on the remaining files & directories
        puts "Working on " + File.join("./_docs", filename)
        out = process_dir(File.join("./_docs", filename))
        #puts "#{out[1]} "
        doc = Kramdown::Document.new(out[1], {auto_ids: true})
        #puts doc.to_html

        markings = "UNCLASSIFIED"

        updateTitle("title_template.html", "title.html", markings, out[0])
        File.write("doc_body.html", doc.to_html)

        
        outfile = out[0].gsub(" ", "_") + ".pdf"

        puts "output file: " + outfile

        system("wkhtmltopdf " +  
            "cover title.html " + 
            "--enable-local-file-access " +
            "toc " + 
            "doc_body.html " + 
            "--enable-local-file-access " +
            "--header-left '#{out[0]}' " + 
            "--header-center #{markings} " + 
            "--footer-center #{markings} " + 
            "--footer-right [page] " + 
            "./#{outfile}")

            File.delete("doc_body.html")
            File.delete("title.html")
    end

#    kit = PDFKit.new(doc.to_html, 
#        :page_size => 'Letter', 
#        :header_font_size => 10,
#        :header_center => "HEADER",
#        :header_left => out[0],
#        :header_line => true, 
#        :footer_font_size => 10,
#        :footer_center => "FOOTER",
#        :footer_right => "[page]", 
#        :footer_line => true,
#        :title => out[0],
#        :toc => true) # toc must be last
#    file = kit.to_file('hello.pdf')
  end
