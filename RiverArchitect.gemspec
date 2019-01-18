Gem::Specification.new do |s|
  s.name          = 'RiverARchitect'
  s.version       = '0.0'
  s.license       = 'GNU General Public License v3.0'
  s.authors       = ['Sebastian Schwindt', 'Gregorz B. Pasternack']
  s.email         = ['sschwindt@ucdavis.edu']
  s.homepage      = 'https://github.com/sschwindt/RiverArchitect/'
  s.summary       = 'River Architect helps designing rivers'

  s.files         = `git ls-files -z`.split("\x0").select do |f|
    f.match(%r{^((.site_package|00_Documentation|HabitatEvaluation|LifespanDesign)/|(LICENSE|README)((\.(md|markdown)|$)))}i)
  end

  s.platform = Gem::Platform::RUBY
end
