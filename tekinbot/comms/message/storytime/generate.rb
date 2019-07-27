require 'marky_markov'
# Choose 2..5 stories.
stories = Dir["corpus/*"].sample(2 + rand(3)) 
# Decide on paragraphs and sentence count.
para_length = []

(2+rand(3)).times { para_length << (3+rand(5))}

markov = MarkyMarkov::TemporaryDictionary.new
# Weight stories differently.
stories.each_with_index {|e,i| (1+i).times {markov.parse_file e}}

story = ""
para_length.each do |e|
	para = markov.generate_n_sentences(e)
	# Find first occurance of period. (Any way to prime?)
	# Later- regex this
	idx = para.index('.')
	next if idx.nil? or para.length <= idx+2
	para = para[idx+2,para.length]
	story << para
	story << "\r\n\r\n"
end
charcters = ["@nomworthy","@jhoak","@logan_w","@nanflasted","@nomworthy","@TekinBot"].sample(3)
story.gsub!("_A_",charcters[0])
story.gsub!("_B_",charcters[1])
story.gsub!("_C_",charcters[2])
puts story