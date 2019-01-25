Gem::Specification.new do |s|
  s.name          = 'RiverArchitect'
  s.version       = '0.0'
  s.license       = 'GNU General Public License v3.0'
  s.authors       = ['Sebastian Schwindt', 'Gregory B. Pasternack']
  s.email         = ['sschwindt@ucdavis.edu']
  s.homepage      = 'https://github.com/sschwindt/RiverArchitect/'
  s.summary       = 'River Architect helps designing rivers'

  s.files         = `git ls-files -z`.split("\x0").select do |f|
    f.match(%r{^((RiverArchitect)/|(LICENSE|README)((\.(md|markdown)|$)))}i)
  end
  
  s.add_development_dependency 'html-proofer', '~> 3.0'
  s.add_development_dependency 'rubocop', '~> 0.50'
  s.add_development_dependency 'w3c_validators', '~> 1.3'
  s.platform = Gem::Platform::RUBY
end
